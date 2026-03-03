import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer
from django.db.models import Sum

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-date', '-created_at')
    serializer_class = ExpenseSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Returns total expenses and a category breakdown.
        """
        total = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Category breakdown
        breakdown = Expense.objects.values('category').annotate(total=Sum('amount')).order_by('-total')
        
        return Response({
            'total_amount': total,
            'category_breakdown': breakdown
        })

    @action(detail=False, methods=['get'])
    def convert_currency(self, request):
        """
        Converts a given amount from a base currency to a target currency using ExchangeRate-API (Fallback from Frankfurter).
        Query params: amount, from (default USD), to (default EUR)
        """
        amount = request.query_params.get('amount')
        base_currency = request.query_params.get('from', 'USD').upper()
        target_currency = request.query_params.get('to', 'EUR').upper()

        if not amount:
            return Response({'error': 'Amount parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            val = float(amount)
        except ValueError:
            return Response({'error': 'Invalid amount provided'}, status=status.HTTP_400_BAD_REQUEST)

        if base_currency == target_currency:
             return Response({'converted_amount': val, 'rate': 1.0, 'currency': target_currency})

        try:
            # Using ExchangeRate-API (v6) as it's often more stable than Frankfurter
            url = f"https://open.er-api.com/v6/latest/{base_currency}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                return Response({'error': f'Base currency {base_currency} not supported'}, status=status.HTTP_404_NOT_FOUND)
            
            response.raise_for_status()
            data = response.json()
            
            if data.get('result') == 'success' and 'rates' in data:
                rate = data['rates'].get(target_currency)
                if rate:
                    return Response({
                        'converted_amount': val * rate,
                        'rate': rate,
                        'currency': target_currency,
                        'base': base_currency
                    })
                else:
                    return Response({'error': f'Target currency {target_currency} not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unexpected response from ExchangeRate-API'}, status=status.HTTP_502_BAD_GATEWAY)
                
        except requests.exceptions.Timeout:
            return Response({'error': 'Currency API timed out'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Currency API error: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        Converts a given amount from a base currency to a target currency using Frankfurter API.
        Query params: amount, from (default USD), to (default EUR)
        """
        amount = request.query_params.get('amount')
        base_currency = request.query_params.get('from', 'USD').upper()
        target_currency = request.query_params.get('to', 'EUR').upper()

        if not amount:
            return Response({'error': 'Amount parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        if base_currency == target_currency:
             return Response({'converted_amount': float(amount), 'rate': 1.0, 'currency': target_currency})

        try:
            # Frankfurter API
            url = f"https://api.frankfurter.app/latest?amount={amount}&from={base_currency}&to={target_currency}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            return Response({
                'converted_amount': data['rates'].get(target_currency),
                'rate': data['rates'].get(target_currency) / float(amount) if hasattr(data, 'rates') else None,
                'currency': target_currency,
                'base': base_currency
            })
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

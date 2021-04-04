from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import Transaction

@login_required(login_url="/login/")
def transactions(request):
    context = {}
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-trx_id')

    return render(
        request,
        'transactions.html',
        {
            'context':{
                'transactions': transactions
            }
        }
    )

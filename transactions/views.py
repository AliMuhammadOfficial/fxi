from django.shortcuts import render, redirect
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
            'context': {
                'transactions': transactions
            }
        }
    )


@login_required(login_url="/login/")
def edit_transaction(request, trx_id):
    if request.method == "GET":
        transaction = Transaction.objects.get(trx_id=trx_id)
        print(transaction)
        return render(
            request,
            "dashboard/edit-transaction.html",
            {
                "context": {
                    "transaction": transaction,
                    "statuses": ["PROCESSING", "COMPLETED", "FAILED"]
                }
            }
        )
    else:
        trx_id = request.POST["trx_id"]
        transaction = Transaction.objects.get(trx_id=trx_id)
        transaction.trx_status = request.POST["trx-status"]
        transaction.save()
        return redirect(to="/dashboard/admin/transactions")

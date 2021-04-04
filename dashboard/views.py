from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import Account
from plans.models import Plan, Investment, RoiAmount
from transactions.models import Transaction
from accounts.models import Action
from earnings.models import Earnings
import uuid
import datetime
from decimal import Decimal


@login_required(login_url="/login/")
def dashboard(request):
    # if request.user.is_superuser:
    #     return redirect('/dashboard/admin')
    try:
        user_account = Account.objects.get(
            user=request.user
        )
    except Account.DoesNotExist:
        user_account = Account.objects.create(
            uid=uuid.uuid4(),
            user=request.user, balance=0
        )
        user_account.save()
    plans = Plan.objects.all()
    investments = Investment.objects.filter(
        user=request.user,
        status="ACTIVE"
    )
    active_investment = 0
    for investment in investments:
        active_investment = active_investment + investment.amount
    context = {
        "plans": plans,
        "account": user_account,
        "active_investment": active_investment,
    }
    return render(
        request,
        "dashboard/dashboard.html",
        {"context": context}
    )


@login_required(login_url="/login/")
def deposit(request):
    if request.method == "POST":
        try:
            deposit_amount = float(request.POST["amount"])
            account = Account.objects.get(user=request.user)
            post_balance = account.balance + deposit_amount
            account.balance = post_balance

            transaction = Transaction(
                user=request.user,
                post_balance=post_balance,
                payment_method="PERFECT_MONEY",
                trx_type="DEPOSIT",
                trx_status="PROCESSING",
                amount=deposit_amount
            )

            action = Action(
                user_friendly_id=str(uuid.uuid4()).split('-')[0],
                user=request.user,
                account=account,
                action_type="DEPOSITED",
                comment=f"{request.user} has successfuly deposited \
                amount of ${deposit_amount}",
                debug_balance=post_balance
            )

            account.save()
            transaction.save()
            action.save()

            return redirect(request.path)
        except Exception as e:
            print("Exception T1 ", e)
            return redirect(request.path)
    else:
        transactions = Transaction.objects.filter(
            user=request.user
        ).exclude(
            trx_type="WITHDRAW"
        ).order_by("-trx_id")
        return render(
            request,
            "payments/deposit.html",
            {
                "context":
                {
                    "transactions": transactions
                }
            }
        )


@login_required(login_url="/login/")
def withdrawal(request):
    if request.method == "POST":
        try:
            withdraw_amount = float(request.POST["amount"])
            account = Account.objects.get(user=request.user)
            post_balance = account.balance - withdraw_amount
            account.balance = post_balance

            transaction = Transaction(
                user=request.user,
                post_balance=post_balance,
                payment_method="PERFECT_MONEY",
                trx_type="WITHDRAW",
                trx_status="PROCESSING",
                amount=withdraw_amount
            )

            action = Action(
                user_friendly_id=str(uuid.uuid4()).split('-')[0],
                user=request.user,
                account=account,
                action_type="WITHDRAWN",
                comment=f"{request.user} has successfuly withdrawn amount of ${withdraw_amount}",
                debug_balance=post_balance
            )

            account.save()
            transaction.save()
            action.save()
            return redirect(request.path)
        except Exception as e:
            print(f"Unexpected error occurred {e}")
            return redirect(request.path)
    else:
        transactions = Transaction.objects.filter(
            user=request.user
        ).exclude(
            trx_type="DEPOSIT"
        ).order_by("-trx_id")
        
        return render(
            request,
            "payments/withdrawal.html",
            {
                "context":
                {
                    "transactions": transactions
                }
            }
        )

@login_required(login_url="/login/")
def admin(request):
    return render(
        request,
        "dashboard/admin.html"
    )

@login_required(login_url="/login/")
def page(request, page):
    page = page.lower()
    if page == "deposits":
        return render(
            request,
            "dashboard/deposits.html"
        )
    elif page == "withdrawals":
        return render(
            request,
            "dashboard/withdrawals.html"
        )
    elif page == "roi":
        if request.method == "GET":
            plans = Plan.objects.all()
            rois = RoiAmount.objects.all()
            plans_list = []

            for plan in plans:
                plans_list.append(RoiAmount.objects.filter(plan=plan))
            
            print(plans_list)
            return render(
                request,
                "dashboard/roi.html",
                {
                    "context": {
                        "plans": plans,
                        "rs": plans_list
                    }
                }
            )
        else:
            print("ROI ID :", request.POST["roi-percent"])
            investments = Investment.objects.filter(status="ACTIVE")
            roi_percent = RoiAmount.objects.get(roi_id=request.POST["roi-percent"])

            for investment in investments:
                try:
                    account = Account.objects.get(user=investment.user)
                    plan_roi = Decimal(investment.amount) * roi_percent.percent
                    account.balance = Decimal(account.balance) + plan_roi
                    account.save()
                    Earnings.objects.create(user=investment.user, earning_type="ROI", amount=plan_roi)

                    print(f"Congratulations {investment.user} you just recieved ${plan_roi} ROI from {investment}")
                except Exception as e:
                    print("Exception ROI R1", e)
            return redirect(request.path)
    elif page == "plans":
        if request.method == "POST":
            name = request.POST["name"]
            minimum = request.POST.get("minimum", 0)
            maximum = request.POST.get("maximum", 0)
            roi = request.POST["roi"]
            period = request.POST["period"]
            plan_period = request.POST["plan-period"]
            capital_return = request.POST.get("capital", False)

            if capital_return == "on":
                capital_ret = True
            else:
                capital_ret = False
            try:
                Plan.objects.create(
                    name=name,
                    minimum=minimum,
                    maximum=maximum,
                    roi=roi,
                    roi_period=period,
                    plan_period=plan_period,
                    capital_return=capital_ret
                )
            except Exception as e:
                print("Error D01", e)

            print(f"""
                Name : {name}
                Minimum : {minimum}
                Maximum : {maximum}
                ROI : {roi}
                Plan Period : {plan_period}
            """)

            return redirect(request.path)
        else:
            plans = Plan.objects.all()
            return render(
                request,
                "dashboard/plans.html",
                {
                    "context": {
                        "plans": plans
                    }
                }
            )
    elif page == "transactions":
        if request.method == "POST":
            start = request.POST["start"]
            end = request.POST["end"]
            trx_id = request.POST["trx-id"]
            trx_type = request.POST["trx-type"].lower()
            trx_status = request.POST["trx-status"].lower()

            if start and end:
                (s_month, s_day, s_year) = start.split("/")
                (e_month, e_day, e_year) = end.split("/")

                if trx_id:
                    transactions = Transaction.objects.filter(
                        Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                        Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                        trx_id=trx_id
                    ).order_by('-trx_time')
                elif trx_id and (trx_type and (not trx_type=="all") and (trx_status and (not trx_status=="all"))):
                    transactions = Transaction.objects.filter(
                        Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                        Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                        trx_status=trx_status.upper(),
                        trx_type=trx_type.upper(),
                        trx_id=trx_id
                    ).order_by('-trx_time')
                elif trx_type and trx_status:
                    if trx_type == "all" and trx_status == "all":
                        transactions = Transaction.objects.filter(
                            Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                            Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                        ).order_by('-trx_time')
                    else:
                        transactions = Transaction.objects.filter(
                            Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                            Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                            trx_status=trx_status.upper(),
                            trx_type=trx_type.upper()
                        ).order_by('-trx_time')

                elif trx_type:
                    if trx_type == "all":
                        transactions = Transaction.objects.filter(
                            Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                            Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                        ).order_by('-trx_time')
                    else:
                        transactions = Transaction.objects.filter(
                            Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                            Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                            trx_type=trx_type.upper(),
                        ).order_by('-trx_time')
                elif trx_status:
                    if trx_status == "all":
                        transactions = Transaction.objects.filter(
                            Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                            Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                        ).order_by('-trx_time')
                    else:
                        transactions = Transaction.objects.filter(
                            Q(trx_date__gte=f"{s_year}-{s_month}-{s_day}"),
                            Q(trx_date__lte=f"{e_year}-{e_month}-{e_day}"),
                            trx_status=trx_status.upper(),
                        ).order_by('-trx_time')
                
            return render(
                request,
                "dashboard/transactions.html",
                {
                    "context": {
                        "transactions": transactions,
                        "filters": {
                            "start": start,
                            "end": end,
                            "trx_id": trx_id,
                            "trx_type": trx_type.capitalize(),
                            "trx_status": trx_status.capitalize()
                        }
                    }
                }
            )

            return redirect(request.path)
        else:
            transactions = Transaction.objects.all().order_by('-trx_time')
            return render(
                request,
                "dashboard/transactions.html",
                {
                    "context": {
                        "transactions": transactions,
                    }
                }
            )
    elif page == "users":
        return render(
            request,
            "dashboard/users.html"
        )
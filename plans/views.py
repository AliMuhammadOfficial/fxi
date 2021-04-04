from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import AccountUser, Account, Action
from plans.models import Plan, Investment
from earnings.models import Earnings


@login_required(login_url="/login/")
def  plans(request):
    if request.method == "GET":
        account = Account.objects.get(
            user=request.user
        )
        plans = Plan.objects.all()
        return render(
            request,
            "plans/plans.html",
            {
                "context": {
                    "plans": plans,
                    "account": account
                }
            }
        )
    else:
        plan_id = request.POST['plan_id']
        investment_amount = float(
            request.POST.get("amount", 0)
        )
        try: # Checked
            account = Account.objects.get(
                user=request.user
            )
            try:
                if account.balance >= float(
                    investment_amount
                ):
                    try:
                        plan = Plan.objects.get(
                        plan_id=plan_id
                    )
                        if (investment_amount >= plan.minimum) and (investment_amount <= plan.maximum):
                            account.balance = account.balance - float(investment_amount)
                            account.save()
                            investment = Investment(
                                user=request.user,
                                plan=plan,
                                amount=investment_amount,
                                interest=0,
                                period=plan.roi_period,
                                status="ACTIVE",
                                return_capital=70
                            )
                            investment.save()
                            # Calculate Bonus Refferal
                            account_user = AccountUser.objects.get(
                                user=request.user
                            )
                            try:
                                level_one_user = AccountUser.objects.get(
                                    uid=account_user.ref_by
                                )
                                try:
                                    level_one_account = Account.objects.get(
                                        user=level_one_user.user
                                    )
                                    level_one_account.balance = level_one_account.balance + \
                                        (investment_amount * 0.05)
                                    level_one_account.save()
                                    Earnings.objects.create(
                                        user=level_one_user.user,
                                        amount=(investment_amount * 0.05),
                                        earning_type="REFERRAL_BONUS"
                                    )
                                except Exception as e:
                                    print("Exception ID P8", e)
                                try:
                                    level_two_user = AccountUser.objects.get(
                                        uid=level_one_user.ref_by
                                    )
                                    try:
                                        level_two_account = Account.objects.get(
                                            user=level_two_user.user
                                        )
                                        level_two_account.balance = level_two_account.balance + \
                                            (investment_amount * 0.03)
                                        level_two_account.save()
                                        Earnings.objects.create(
                                            user=level_two_user.user,
                                            amount=(investment_amount * 0.03),
                                            earning_type="REFERRAL_BONUS"
                                        )
                                    except Exception as e:
                                        print("Exception ID P6", e)
                                    try:
                                        level_three_user = AccountUser.objects.get(
                                            uid=level_two_user.ref_by
                                        )
                                        try:
                                            level_three_account = Account.objects.get(
                                                user=level_three_user.user
                                            )
                                            level_three_account.balance = level_three_account.balance + \
                                                (investment_amount * 0.01)
                                            level_three_account.save()
                                            Earnings.objects.create(
                                                user=level_three_user.user,
                                                amount=(investment_amount * 0.01),
                                                earning_type="REFERRAL_BONUS"
                                            )
                                        except Exception as e:
                                            print("Exception ID P6", e)
                                        try: 
                                            level_four_user = AccountUser.objects.get(
                                                uid=level_three_user.ref_by
                                            )
                                            try:
                                                level_four_account = Account.objects.get(
                                                    user=level_four_user.user
                                                )
                                                level_four_account.balance = level_four_account.balance + \
                                                    (investment_amount * 0.01)
                                                level_four_account.save()
                                                Earnings.objects.create(
                                                    user=level_four_user.user,
                                                    amount=(investment_amount * 0.01),
                                                    earning_type="REFERRAL_BONUS"
                                                )
                                            except Exception as e:
                                                print("Exception ID P9", e)
                                            try:
                                                level_five_user = AccountUser.objects.get(
                                                    uid=level_four_user.ref_by
                                                )
                                                try:
                                                    level_five_account = Account.objects.get(
                                                        user=level_five_user.user
                                                    )
                                                    level_five_account.balance = level_five_account.balance + \
                                                        (investment_amount * 0.01)
                                                    level_five_account.save()
                                                    Earnings.objects.create(
                                                        user=level_five_user.user,
                                                        amount=(investment_amount * 0.01),
                                                        earning_type="REFERRAL_BONUS"
                                                    )
                                                    print(f"""
                                                        {level_one_user}, 
                                                        {level_two_user}, 
                                                        {level_three_user},
                                                        {level_four_user},
                                                        {level_five_user}"""
                                                    )
                                                except Exception as e:
                                                    print("Exception ID P_10", e)
                                            except Exception as e:
                                                print("Exception ID P5", e)
                                        except Exception as e:
                                            print("Exception ID P4", e)
                                    except Exception as e:
                                        print("Exception ID P3", e)
                                except Exception as e:
                                    print("Exception ID P2", e)
                            except Exception as e:
                                print(f"Exception ID P_1", e) 
                        else: #Checked
                            # THROW ERROR MESSAGE : 
                            # invalid amoutn to purchase plan
                            msg = f"To purchase this plan you must \
                                invest between {plan.minimum} - {plan.maximum}"
                            print(msg)
                    except Plan.DoesNotExist: # Checked
                        msg = f"Error P4 | Plan with {plan_id} does not exist"
                        print(msg)
                else:
                    msg = "Insuficient Balance"
                    print(msg)
            except Exception as e: 
                msg = "Error P3 | Invalid amount! please enter \
                    valid amoutn to purchase the plan!"
                print(msg, e) # Investment Amount Value Error
        except Account.DoesNotExist: # Checked
            msg = f"Error P2 | Account for {request.user} does not exist"
            print(msg)
        except Exception as e:
            print(f"Error P1 | {e}")
        return redirect(request.path)


@login_required(login_url="/login/")
def active(request):
    if request.method == "GET":
        try:
            investments = Investment.objects.filter(
                user=request.user, status="ACTIVE"
            )
            print("Invest : ", investments)
        except Exception as e:
            print("Exception : ", e)
        return render(
            request,
            "plans/investments.html",
            {
                "context": {
                    "investments": investments
                }
            }
        )
    else:
        investment_id = request.POST["investment_id"]
        account = Account.objects.get(
            user=request.user
        )
        investment = Investment.objects.get(
            user=request.user,
            investment_id=investment_id,
            status="ACTIVE"
        )
        capital = investment.amount * (investment.return_capital / 100)
        
        investment.status = "INACTIVE"
        investment.save()
        account.balance = float(account.balance) + float(capital)
        account.save()
        
        print("Invest ID: ", request.POST['investment_id'])
        return redirect(request.path)


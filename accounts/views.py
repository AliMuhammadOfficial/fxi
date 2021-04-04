from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import AccountUser
from plans.models import Plan, Investment

@login_required(login_url="/login/")
def account(request):

    try:
        account = AccountUser.objects.get(user=request.user)
    except AccountUser.DoesNotExist:
        account = AccountUser.objects.create(user=request.user)
        print(f"Account does not exist for user {request.user}")
        return redirect(request.path)
    return render(
        request,
        'user-profile.html',
        {
            "context": {
                "account": account
            }
        }
    )


@login_required(login_url="/login/")
def team(request):
    teams = []
    team_business = 0
    direct_business = 0
    try:
        account_user = AccountUser.objects.get(
            user=request.user
        )
        directs = AccountUser.objects.filter(
            ref_by=account_user.uid
        )
        level_one_users = AccountUser.objects.filter(
            ref_by=account_user.uid
        )
        for level_one_user in level_one_users:
            teams.append({
                "member": level_one_user,
                "level": 1
            })
            for level_two_user in AccountUser.objects.filter(
                    ref_by=level_one_user.uid
                ):
                    teams.append({
                        "member": level_two_user,
                        "level": 2
                    })
                    try:
                        level_two_investments = Investment.objects.get(
                            user=level_two_user.user,
                            status="ACTIVE"
                        )
                        team_business = team_business + level_two_investments.amount
                    except Investment.DoesNotExist:
                        print("Error T2 Invest Does not exist.")
                    for level_three_user in AccountUser.objects.filter(
                            ref_by=level_two_user.uid
                        ):
                            # print("level_three_user:  ", level_three_user)
                            teams.append({
                                "member": level_three_user,
                                "level": 3
                            })
                            try:
                                level_three_investments = Investment.objects.get(
                                    user=level_three_user.user,
                                    status="ACTIVE"
                                )
                                team_business = team_business + level_three_investments.amount
                            except Investment.DoesNotExist:
                                print("Error T3 Invest Does not exist.")
                            for level_four_user in AccountUser.objects.filter(
                                    ref_by=level_three_user.uid
                                ):
                                    # print("level_four_user:  ", level_four_user)
                                    teams.append({
                                        "member": level_four_user,
                                        "level": 4
                                    })
                                    try:
                                        level_four_investments = Investment.objects.get(
                                            user=level_four_user.user,
                                            status="ACTIVE"
                                        )
                                        team_business = team_business + level_four_investments.amount
                                    except Investment.DoesNotExist:
                                        print("Error T4 Inevst Does not Exist")
                                    for level_five_user in AccountUser.objects.filter(
                                            ref_by=level_four_user.uid
                                        ):
                                            # print("level_five_user:  ", level_five_user)
                                            teams.append({
                                                "member": level_five_user,
                                                "level": 5
                                            })
                                            try:
                                                level_five_investments = Investment.objects.get(
                                                    user=level_five_user.user,
                                                    status="ACTIVE"
                                                )
                                                team_business = team_business + level_five_investments.amount
                                            except Investment.DoesNotExist:
                                                print("Error T5 Invest Does not exist")
        print("Teams : ", teams)
        return render(
            request,
            'team.html',
            {
                "context": {
                "user": account_user,
                "directs": directs,
                "teams": teams,
                "team_business": team_business,
                "direct_business": direct_business,
                }
            }
        )
    except AccountUser.DoesNotExist:
        account_user = AccountUser(
            user=request.user
        )
        account_user.save()
        print("User Does Not Exist")
        # account_user = AccountUser(user=request.user)
        return render(
            request,
            'team.html',
            {
                "context": {"user": account_user}
            }
        )
    except Exception as e:
        print(f"Unexoected error Occurrred {e}")
        return redirect(request.path)

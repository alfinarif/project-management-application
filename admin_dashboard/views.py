from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class AdminDashboardTemplateAPIView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'admin':
                context = {

                }
                return render(request, 'index.html', context)

            elif request.user.user_type == 'leader':
                return redirect('leader:leader_dashboard')

            elif request.user.user_type == 'worker':
                return redirect('worker:worker_dashboard')
                
            else:
                return redirect('accounts:login')

        else:
            return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        pass

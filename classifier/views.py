from django.views.generic.edit import FormView

from .forms import MailForm
from .ml import predict_mail

class MailClassifierView(FormView):
    template_name = 'classifier/home.html'
    form_class = MailForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('prediction', None)
        return context

    def form_valid(self, form):
        prediction = predict_mail(form.cleaned_data['message'])
        context = self.get_context_data(form=form, prediction=prediction)
        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

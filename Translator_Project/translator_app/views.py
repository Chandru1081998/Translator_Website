from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Translation
from deep_translator import GoogleTranslator


class TranslateView(TemplateView):
    template_name = 'translator_app/translate.html'

    def post(self, request, *args, **kwargs):
        original_text = request.POST.get('original_text')
        language_from = request.POST.get('language_from')
        language_to = request.POST.get('language_to')

        if not (original_text and language_from and language_to):
            context = {
                'error_message': 'Please provide original text, source language, and target language.'
            }
            return render(request, self.template_name, context)

        translator = GoogleTranslator(source=language_from, target=language_to)
        translated_text = translator.translate(original_text)

        translation = Translation.objects.create(
            original_text=original_text,
            translated_text=translated_text,
            language_from=language_from,
            language_to=language_to
        )

        context = {
            'translation': translation
        }

        return render(request, self.template_name, context)

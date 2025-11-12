from django import forms


class PaymentForm(forms.Form):
    """Formulario para procesar pagos con tarjeta de crédito/débito."""
    
    # Información de la tarjeta
    card_number = forms.CharField(
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '1234 5678 9012 3456',
            'maxlength': '19',
            'pattern': '[0-9\s]*'
        }),
        label='Número de tarjeta'
    )
    
    card_holder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Nombre como aparece en la tarjeta'
        }),
        label='Nombre del titular'
    )
    
    expiry_month = forms.ChoiceField(
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Mes de expiración'
    )
    
    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2025, 2035)],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Año de expiración'
    )
    
    cvv = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '123',
            'maxlength': '4',
            'pattern': '[0-9]*'
        }),
        label='CVV'
    )
    
    # Información de facturación
    billing_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Dirección de facturación'
        }),
        label='Dirección de facturación'
    )
    
    billing_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ciudad'
        }),
        label='Ciudad'
    )
    
    billing_postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Código postal'
        }),
        label='Código postal'
    )
    
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-100',
            'readonly': True
        }),
        label='Monto a pagar'
    )

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number', '').replace(' ', '')
        if not card_number.isdigit():
            raise forms.ValidationError('El número de tarjeta debe contener solo dígitos.')
        if len(card_number) < 13 or len(card_number) > 19:
            raise forms.ValidationError('El número de tarjeta debe tener entre 13 y 19 dígitos.')
        return card_number
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv', '')
        if not cvv.isdigit():
            raise forms.ValidationError('El CVV debe contener solo dígitos.')
        if len(cvv) < 3 or len(cvv) > 4:
            raise forms.ValidationError('El CVV debe tener 3 o 4 dígitos.')
        return cvv
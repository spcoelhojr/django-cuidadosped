var currencyMaskBehavior = function(val) {
    return '000.000.000.000.000,00';
},
currencyOptions = {
    reverse: true,
    onKeyPress: function(val, e, field, options) {
        field.mask(currencyMaskBehavior.apply({}, arguments), options);
    }
};

django.jQuery(function(){
    django.jQuery('.mask-price').mask(currencyMaskBehavior, currencyOptions);

    django.jQuery('#appointmentfinancials_form').submit(function(){
        django.jQuery('#appointmentfinancials_form').find(":input[class*='mask-']").unmask();
    });
});
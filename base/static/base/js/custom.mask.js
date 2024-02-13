/**
 * @return {string}
 */
var SPMaskBehavior = function (val) {
  return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(SPMaskBehavior.apply({}, arguments), options);
    }
};

django.jQuery(function(){
    django.jQuery('.mask-phone_number').mask(SPMaskBehavior, spOptions);
    django.jQuery('.mask-cpf').mask('000.000.000-00', {reverse: true});

    django.jQuery('#medic_form').submit(function(){
        django.jQuery('#medic_form').find(":input[class*='mask-']").unmask();
    });

    django.jQuery('#secretary_form').submit(function(){
        django.jQuery('#secretary_form').find(":input[class*='mask-']").unmask();
    });

    django.jQuery('#relative_form').submit(function(){
        django.jQuery('#relative_form').find(":input[class*='mask-']").unmask();
    });

    django.jQuery('#patient_form').submit(function(){
        django.jQuery('#patient_form').find(":input[class*='mask-']").unmask();
    });

    django.jQuery('#patients-group').submit(function(){
        django.jQuery('#patient-group').find(":input[class*='mask-']").unmask();
    });
});



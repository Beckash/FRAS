function get_departments(){
            new Ajax.Request('load_departments', {
            method: 'post',
            parameters: $H({'college':$('college').getValue()}),
            onSuccess: function(transport) {
                var e = $('department')
                if(transport.responseText)
                    e.update(transport.responseText)
            }
            }); // end new Ajax.Request
        }
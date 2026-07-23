$("#college").change(function () {
        const collegeId = $(this).val();  // get the selected subject ID from the HTML dropdown list
        $.ajax({                       // initialize an AJAX request
            type: "POST",
            url: '{% url "load_departments" %}',
            data: {
                'college_id': collegeId       // add the country id to the POST parameters
            }
             })

             .done(function(response){
                var json_data=JSON.parse(response);
                console.log(json_data)
                //Displaying Attendance Date Input and Students Attendance
                var div_data='';
                for(key in json_data)
                {
                    div_data+="<option value='"+ json_data[key]['id'] +"'>"+ json_data[key]['name']+" </option>";

                }
                $("#department").html(div_data);

            })
            .fail(function(){
                alert("Error in Fetching Students.")
            })
        });
/*
 * Author: Abdullah A Almsaeed
 * Date: 4 Jan 2014
 * Description:
 *      Dashboard main JS - fixed sortable error and ready for AJAX
 **/

$(function () {
  'use strict'

  // === FIXED: Only initialize sortable if jQuery UI is loaded ===
  if ($.ui && $.ui.sortable) {
    // Make the dashboard widgets sortable
    $('.connectedSortable').sortable({
      placeholder: 'sort-highlight',
      connectWith: '.connectedSortable',
      handle: '.card-header, .nav-tabs',
      forcePlaceholderSize: true,
      zIndex: 999999
    })
    $('.connectedSortable .card-header, .connectedSortable .nav-tabs-custom').css('cursor', 'move')

    // jQuery UI sortable for the todo list
    $('.todo-list').sortable({
      placeholder: 'sort-highlight',
      handle: '.handle',
      forcePlaceholderSize: true,
      zIndex: 999999
    })
  }

  // === Summernote editor ===
  if ($('.textarea').length) {
    $('.textarea').summernote()
  }

  // === Date range picker ===
  if ($('.daterange').length) {
    $('.daterange').daterangepicker({
      ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      },
      startDate: moment().subtract(29, 'days'),
      endDate: moment()
    }, function (start, end) {
      window.alert('You chose: ' + start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))
    })
  }

  // === jQuery Knob ===
  if ($('.knob').length) {
    $('.knob').knob()
  }

  // === World map data ===
  var visitorsData = {
    'US': 398, 'SA': 400, 'CA': 1000, 'DE': 500,
    'FR': 760, 'CN': 300, 'AU': 700, 'BR': 600,
    'IN': 800, 'GB': 320, 'RU': 3000
  }

  if ($('#world-map').length) {
    $('#world-map').vectorMap({
      map: 'usa_en',
      backgroundColor: 'transparent',
      regionStyle: {
        initial: {
          fill: 'rgba(255, 255, 255, 0.7)',
          'fill-opacity': 1,
          stroke: 'rgba(0,0,0,.2)',
          'stroke-width': 1,
          'stroke-opacity': 1
        }
      },
      series: {
        regions: [{
          values: visitorsData,
          scale: ['#ffffff', '#0154ad'],
          normalizeFunction: 'polynomial'
        }]
      },
      onRegionLabelShow: function (e, el, code) {
        if (typeof visitorsData[code] != 'undefined')
          el.html(el.html() + ': ' + visitorsData[code] + ' new visitors')
      }
    })
  }

  // === Sparklines ===
  if ($('#sparkline-1').length) {
    var sparkline1 = new Sparkline($("#sparkline-1")[0], { width: 80, height: 50, lineColor: '#92c1dc', endColor: '#ebf4f9' });
    var sparkline2 = new Sparkline($("#sparkline-2")[0], { width: 80, height: 50, lineColor: '#92c1dc', endColor: '#ebf4f9' });
    var sparkline3 = new Sparkline($("#sparkline-3")[0], { width: 80, height: 50, lineColor: '#92c1dc', endColor: '#ebf4f9' });

    sparkline1.draw([1000, 1200, 920, 927, 931, 1027, 819, 930, 1021]);
    sparkline2.draw([515, 519, 520, 522, 652, 810, 370, 627, 319, 630, 921]);
    sparkline3.draw([15, 19, 20, 22, 33, 27, 31, 27, 19, 30, 21]);
  }

  // === Calendar ===
  if ($('#calendar').length) {
    $('#calendar').datetimepicker({
      format: 'L',
      inline: true
    })
  }

  // === Chat box scroll ===
  if ($('#chat-box').length) {
    $('#chat-box').overlayScrollbars({ height: '250px' })
  }

  // === Chart.js examples ===
  function initLineChart(canvasId, labels, data, borderColor, fillColor) {
    if ($(canvasId).length) {
      var ctx = $(canvasId)[0].getContext('2d');
      return new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: '',
            data: data,
            borderColor: borderColor,
            backgroundColor: fillColor,
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 7,
            lineTension: 0
          }]
        },
        options: { responsive: true, maintainAspectRatio: false, legend: { display: false } }
      });
    }
  }

  // Example charts (keep your data as before)
  initLineChart('#revenue-chart-canvas',
    ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    [28, 48, 40, 19, 86, 27, 90],
    'rgba(60,141,188,0.9)', 'rgba(60,141,188,0.8)'
  )

  // === Subjects AJAX loader ===
  $("#section, #batch").change(function () {
    var batch = $("#batch").val();
    var section = $("#section").val();

    if (batch && section) {
      console.log("Batch:", batch, "Section:", section); // debug log
      $.ajax({
        url: '/load_subjects_section_batch/',
        type: 'POST',
        data: {
          'batch': batch,
          'section': section,
          'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function (data) {
          var options = '<option selected disabled>-- choose a subject --</option>';
          data.forEach(function (item) {
            options += '<option value="' + item.id + '">' + item.name + '</option>';
          });
          $("#subject").html(options);
        },
        error: function (xhr, status, error) {
          console.log("AJAX Error:", status, error);
          $("#subject").html('<option>-- Error loading subjects --</option>');
        }
      });
    }
  });
});

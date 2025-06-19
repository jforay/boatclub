document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');  // Using ID again
    
    if (calendarEl) {
        var marinaId = calendarEl.getAttribute('data-marina-id')
        var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth'
        },
        // Block all Mondays (Monday = 1)
        dayCellClassNames: function(arg) {
            if (arg.date.getDay() === 1) {
                return 'monday-disabled';  // Class to style and disable Mondays
            }
        },
    
        dateClick: function(info) {
            var clickedDate = new Date(info.date);
            if (clickedDate.getDay() == 1){
                alert('Bookings are not available on Mondays.');
                return;
            }

            
    
            window.location.href = `/reservations/${marinaId}/${info.dateStr}`;
        }
        });
    
        calendar.render();
    }
    });
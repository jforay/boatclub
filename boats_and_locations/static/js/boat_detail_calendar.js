document.addEventListener('DOMContentLoaded', function() {
var calendarEl = document.getElementById('calendar');  // Using ID again

if (calendarEl) {
    var today = new Date();
    var firstAvailableDate = new Date(today.getFullYear(), today.getMonth(), today.getDate()+2)
   
    var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth'
    },

    validRange: {
        start: firstAvailableDate
    },

    events: calendarEvents.map( event => ({
        title: event.text,
        start: event.date,
        display: 'list-item'

    })),
    // Block all Mondays (Monday = 1)
    dayCellClassNames: function(arg) {
        if (arg.date.getDay() === 1) {
            return 'monday-disabled';  // Class to style and disable Mondays
        }
    },

    dateClick: function(info) {
        var clickedDate = new Date(info.date);
        var boatID = window.location.pathname.split('/')[2];
        if (clickedDate.getDay() == 1){
            alert('Bookings are not available on Mondays.');
            return;
        }
        if(clickedDate < firstAvailableDate){
            alert("You cannot make a reservation for this day.");
            return;
        }

        window.location.href = `/boats/${boatID}/${info.dateStr}`;
    }
    });

    calendar.render();
}
});
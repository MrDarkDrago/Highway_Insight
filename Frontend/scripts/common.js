

$(document).ready(function () {
  $(".select2-ajax").each(function () {
    $(this).select2({
      width: '100%',  // Ensures full responsiveness
      ajax: {
        url: $(this).data("url"),  // Get URL from data attribute
        dataType: "json",
        delay: 250,
        processResults: function (data) {
          return {
            results: data.map((item) => ({
              id: item.id,  // Adjust based on API response
              text: item.text,  // Adjust based on API response
            })),
          };
        },
        cache: true,
      },
      placeholder: "Select an option",
      allowClear: true,
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  let dateInput = document.querySelector(".date");

  if (dateInput) {
      flatpickr(".date", {
          dateFormat: "Y-m-d", // YYYY-MM-DD format
          altInput: true,
          altFormat: "F j, Y", // Pretty format: February 16, 2025
          minDate: "today", // Disable past dates
          defaultDate: "today", // Set today's date as default
          disableMobile: true, // Use native picker on mobile
          onChange: function (selectedDates, dateStr) {
              let selectedDate = luxon.DateTime.fromISO(dateStr);
              console.log("Formatted Date:", selectedDate.toFormat("MMMM dd, yyyy"));

              // Check if a date is selected and update the UI accordingly
              if (!dateStr) {
                  document.querySelector("#date-message").textContent = "Please select a date.";
              } else {
                  document.querySelector("#date-message").textContent = "";
              }
          }
      });
  }
});

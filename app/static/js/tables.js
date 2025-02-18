$(document).ready(function () {
    $('table').DataTable({
        "paging": true,
        "searching": true,
        "ordering": true,
        "lengthChange": true,
        "pageLength": 10,
        "responsive": true,
        "autoWidth": true 
    });
});
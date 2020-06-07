$(document).ready(function () {
    $("input[name=type]").on("click", function () {
        const type = $(this).val();
        const newPrice = $(this).data("price");
        // change price in text field and in data attr
        $(this).closest("div.card-body").find(".price").text(newPrice);
        $(this).closest("div.card-body").attr("data-price", type);

        // console.log($(this).text());
        // $.ajax({
        //     type: "GET",
        //     url: "getEvents",
        //     data:{
        //         type: type,
        //         group: group
        //     },
        //     success: function(response){
        //         price = response.price
        //         console.log(price)
        //         // code to change price in front end
        //     }
        // })

        // const type = $("input[name=type]:checked").val(); // sm ot lg

        // if (type == "sm") {
        //     $(document).on("change", ".update_price", function () {
        //         var sum = 0;

        //         $(".price span").text(sum.toFixed(2));
        //     });
        // }
        // if (type == "lg") {
        //     $(document).on("change", ".update_price", function () {
        //         var sum = 0;

        //         $(".club_product_price span").text(sum.toFixed(2));
        //     });
        // }
    });

    $(".groups .nav-link").on("click", function () {

        // hightlight chosen category on nav bar
        $(".groups").find(".active").removeClass("active");
        $(this).addClass("active");

        // filter
        const filter = $(this).data("group");
        cards = $(".card");
        if (filter === "All") {
            cards.parent().show();
            return;
        }
        cards.parent().hide();

        const titles = $(".group:contains(" + filter + ")");
        titles.closest(".card").parent().show();

    });
});

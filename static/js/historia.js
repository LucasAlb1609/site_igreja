$(document).ready(function(){
    // Carrossel para a seção de Pastorado
    $('.pastor-carousel').slick({
        slidesToShow: 3, // Reduzido para 3 para acomodar cards maiores
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        arrows: true,
        dots: true,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });

    // Carrossel para a seção do Memorial
    $('.memorial-carousel').slick({
        slidesToShow: 4, // Reduzido para 4 para acomodar cards maiores
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2500,
        arrows: false,
        dots: true,
        responsive: [
             {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
});

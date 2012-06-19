$(document).ready(function() {

			$("#add").hide();
			$(".ocultar").hide();
			$("#mostrar").click(function (){
				$(this).hide();
				$("#add").fadeIn("slow");
				$(".ocultar").fadeIn("slow");
				e.preventDefault();
			});
			/*
			Change the given value to the corresponding image.
			*/
			$(".n1").each(function (i, obj) {
				if ( $(this).text() == 0)
					$(this).html("<i class=\"icon-minus\"></i>")
				else if ($(this).text() == 1)
					$(this).html("<i class=\"icon-ok\"></i>")
				else
					$(this).html("<i class=\"icon-remove\"></i>")
			})

			$(".n2").each(function (i, obj) {
				if ( $(this).text() == 0)
					$(this).html("<i class=\"icon-minus\"></i>")
				else if ($(this).text() == 1)
					$(this).html("<i class=\"icon-ok\"></i>")
				else
					$(this).html("<i class=\"icon-remove\"></i>")
			})

});
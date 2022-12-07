$(function(){

// 자주묻는질문 열기/닫기
	$('.btn_faq').click(function(){
		if($(this).hasClass('on')){
			faq_hide();	
		}else{
			faq_show();
		};
		return false;
	});

	//열기
	function faq_show(){
		$('.btn_faq').addClass('on').attr('title','자주 묻는 질문 닫기');
		$('.faq_wrap').slideDown('fast').focus();;
		$('.modal_blanklink').remove();
		$('.accessibility_blank').append("<a href='#' class='modal_blanklink'>포커스이동</a>");

		$('.btn_close_faq').click(function(){
			faq_hide();	
		});
	};

	//닫기
	function faq_hide(){
		$('.btn_faq').removeClass('on').attr('title','자주 묻는 질문 열기');
		$('.faq_wrap').slideUp(150);	
		$('.accessibility_blank').find(".modal_blanklink").remove();
	};
	
//자주묻는질문/보내기 포커스 이동

	//tab 순환
	$(document).on("focus",".accessibility_blank .modal_blanklink",function(){  
		$('.accessibility_blank').find('.faq_wrap').focus();
	});

	//shift+tab 순환
	$(document).on('keydown', function(e){
		if(e.shiftKey && e.keyCode == 9 && $('.faq_wrap').is(':focus')) {
			 e.preventDefault();
			$('.btn_send').focus();
		};
	});

//캐로셀
	$(window).on('load', function() {	//웹폰트 로드 후 실행

		//캐로셀 (none)
		$('.owl-carousel.none').owlCarousel({
			loop:false,
			autoWidth:false,
			margin:10,
			nav:false,
			dots:false,
			items:2,
			smartSpeed:400
		})	;

		//캐로셀 (none-auto)
		$('.owl-carousel.none-auto').owlCarousel({
			loop:false,
			autoWidth:true,
			margin:10,
			nav:false,
			dots:false,
			items:3,
			smartSpeed:400
		})	;

		//캐로셀 (nav)
		$('.owl-carousel.nav').owlCarousel({
			loop:false,
			autoWidth:false,
			margin:10,
			nav:true,
			dots:false,
			items:2,
			smartSpeed:400
		})	;

		//캐로셀 (nav-auto)
		$('.owl-carousel.nav-auto').owlCarousel({
			loop:false,
			autoWidth:true,
			margin:10,
			nav:true,
			dots:false,
			items:3,
			smartSpeed:400
		})	;

		//캐로셀 (dot)
		$('.owl-carousel.dot').owlCarousel({
			loop:false,
			autoWidth:false,
			margin:10,
			nav:false,
			dots:true,
			items:2,
			smartSpeed:400
		})	;

		//캐로셀 (dot-auto)
		$('.owl-carousel.dot-auto').owlCarousel({
			loop:false,
			autoWidth:true,
			margin:10,
			nav:false,
			dots:true,
			items:3,
			smartSpeed:400
		})	;

		//캐로셀 (dot-img)
		$('.owl-carousel.dot-img').owlCarousel({
			loop:false,
			autoWidth:true,
			margin:10,
			nav:false,
			dots:true,
			items:1,
			autoHeight:true,
			smartSpeed:400
		})	;

		//캐로셀 (nav-img)
		$('.owl-carousel.nav-img').owlCarousel({
			loop:false,
			autoWidth:true,
			margin:10,
			nav:true,
			dots:false,
			items:1,
			autoHeight:true,
			smartSpeed:400
		})	;

		//캐로셀 (none-img)
		$('.owl-carousel.none-img').owlCarousel({
			loop:false,
			autoWidth:true,
			margin:10,
			nav:false,
			dots:false,
			items:1,
			autoHeight:true,
			smartSpeed:400
		})	;
	});

//메뉴
	$('.btn_menu').click(function(){
		if($(this).hasClass('on')){
			$(this).removeClass('on');
			$('.head_menu').hide(); 
		}else{
			$(this).addClass('on');
			$('.head_menu').fadeIn('fast');
		};
		return false;
	});

//배경클릭시
	$('html').click(function() {
		if($('.btn_menu').hasClass('on')){
			$('.btn_menu').click();
		};
	});

//피드백 : 스마일	
	$.fn.feedback_smile=function() {
		if($(this).hasClass('on')){
			$(this).removeClass('on');
		}else{
			$(this).closest('ul').find('.btn_smile').removeClass('on');
			$(this).addClass('on');			
		};
	};

// Number 버튼형 
	$('.btn_qty').click(function(){
		var q_input = $(this).closest('.number_wrap').children('input');
		var q_min = q_input.attr('min');
		var q_max = q_input.attr('max');

		if($(this).hasClass('qty_p')){
			if(q_input.val()<q_max){
				q_input.val(parseInt(q_input.val())+1)
			}else{
				alert('값이 ' + q_max + '보다 작아야 합니다.');
			};
		}else{
			if(q_input.val()>q_min){
				q_input.val(parseInt(q_input.val())-1)
			}else{
				alert('값이 ' + q_min + '보다 커야 합니다.');
			};
		};
		return false;
	});


//모달 열기
	$('.btn_bot_modal').click(function(){

		var modal_id = $(this).attr('name');
		var modal_type = $(this).attr('modal-type');
		$('#'+modal_id).addClass(modal_type);

		if(modal_type!='slide'){
			$('#'+modal_id).fadeIn('fast');
		}else if(modal_type=='slide'){
			$('#'+modal_id).fadeIn('fast');
		};

		modal_position(modal_id);

		$(window).resize(function() {
			modal_position(modal_id);
		});
	});


//모달 닫기 및 초기화
	$('.btn_modal_close').click(function(){
		$(this).closest('.chat_modal').fadeOut('fast', function(){
			$(this).closest('.chat_modal').removeClass('full1 full2 flexible slide');		
			$(this).closest('.chat_modal').find('.chat_modal_cont').css('max-height','');
			$(this).closest('.chat_modal').find('.chat_modal_in').css({'margin-left':'','margin-top':'','left':'','top':'','bottom':''});
		});

		if($(this).closest('.chat_modal').hasClass('slide')){
			$(this).closest('.chat_modal').find('.chat_modal_in').css('bottom','-100%');		
		};
	});


//모달 높이/마진
	modal_position = function(modal_id) {

		//flexible 일 경우
		if($('#'+modal_id).hasClass('flexible')){

			var browser_height = $(window).height()-200;
			$('#'+modal_id).find('.chat_modal_cont').css('max-height',browser_height+'px');

			var modal_height = $('#'+modal_id).children('.chat_modal_in').outerHeight() / 2;
			$('#'+modal_id).children('.chat_modal_in').css('margin-top','-'+modal_height+'px');

			var modal_width = $('#'+modal_id).children('.chat_modal_in').outerWidth() / 2;
			$('#'+modal_id).children('.chat_modal_in').css('margin-left','-'+modal_width+'px').css({'left':'50%','top':'50%'});

		//slide 일 경우
		}else if ($('#'+modal_id).hasClass('slide')){
			var browser_height = $(window).height()-150;
			$('#'+modal_id).find('.chat_modal_cont').css('max-height',browser_height+'px');
			$('#'+modal_id).children('.chat_modal_in').css('bottom','0');
		};
	};

});





//자동완성
	var dq_acLine = 4;	//자동완성 갯수 + 1

	function handleEnter(e){	

		if($('#auto_complete').is(':visible')){

			if (window.event) {
				e = window.event;
			};
			
			if(e.keyCode == 13 || e.which == 13 || e.keyCode == 0 || e.which == 0  ) {
				//goSearch();
				return;

			} else if(e.keyCode == 40 || e.which == 40 || e.keyCode == 38 || e.which == 38 || e.shiftKey || e.keyCode == 9) {
				
				if($("#auto_complete").find(">li").length > 0) {
						
					if(e.keyCode == 40 || e.which == 40 || e.shiftKey && e.keyCode == 9 ){	// Down & Shift+Tab

						if(dq_acLine < $("#auto_complete").find(">li").length + 1){
							e.preventDefault();
							dq_acLine++;
						};

					}else if(e.keyCode == 38 || e.which == 38  || e.keyCode == 9 ){		// Up or Tab

						e.preventDefault();

						if(dq_acLine > 1){
							dq_acLine--;
						}else if (dq_acLine == 1){
							$('#auto_complete').hide();
						};
					};

					$("#auto_complete li").each( function(index) {
						 if((index+1) == dq_acLine){
							$(this).find("a").addClass("on");
							$("#send_input").val($(this).find("a").text());
						} else{
							$(this).find("a").removeClass("on");
						};
					 });				
				} else {
					dq_acLine = $("#auto_complete").find(">li").length+1;
				};

			} else {
				dq_acLine = $("#auto_complete").find(">li").length+1;
			};
		
		};

	};

	$(function(){
		$('#send_input').focusout(function(){
			$('#auto_complete').hide();
		});
	})
$(document).ready(function(){

	function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	console.log('Document is ready');

	//localStorage.removeItem('token');

	//user click on sign-in button on homepage
	/*
	$('#toggle-signin').click(function(e){
		e.preventDefault();
		if(localStorage.getItem('token')===null){
			$.mobile.changePage("index2.html#signup_page")
		}
		else{
			$.mobile.changePage("index2.html#innovators_page");
		}

	});
	*/

	$('#toggle-login').click(function(e){
		console.log('login button clicked');
		/*
		e.preventDefault();
		if(localStorage.getItem('token')==null){
			console.log('token found with null value');
			$.mobile.changePage('index2.html#login_page');
		}
		else{
			console.log('token: '+localStorage.getItem('token'));
			$.mobile.changePage('index2.html#innovators_page');
		}
		*/
	});

	$('#signup_request').click(function(e){
		var details = {
			username: null,
			password: null
		};

		details.username = $('#username_signup_input').val();
		details.password = $('#password_signup_input').val();

		console.log('username: '+details.username);
		console.log('password: '+details.password);

		$.ajax({
			type: 'POST',
			url: 'http://atcserver.herokuapp.com/signup/',
			data: details,
			success: function(data){
				new $.nd2Toast({
                    message : "Sign Up successful",
                    ttl : 3000
                });
                $.ajax({
					type: 'POST',
					url: 'http://atcserver.herokuapp.com/api-token-auth/',
					data: details,
					success: function(data){
					localStorage.setItem('token',data.token);
					new $.nd2Toast({
                    	message : data.token,
                    	ttl : 3000
                	});
                	$.mobile.changePage('http://atcserver.herokuapp.com/#innovators_page');
					}
					});
				},
				error: function(e){
				new $.nd2Toast({
                    message : 'Sign up failed: ',
                    ttl : 3000
                });
			}
		});

	});

	$('#login_request').click(function(e){
		e.preventDefault();
		var details = {
			username: null,
			password: null
		};

		details.username = $('#username_input').val();
		details.password = $('#password_input').val();

		console.log('username: '+details.username);
		console.log('password: '+details.password);

		$.ajax({
			type: 'POST',
			beforeSend: function(xhr){
					xhr.setRequestHeader("HTTP_X_CSRFTOKEN ",csrftoken);
				},
			url: 'http://atcserver.herokuapp.com/api-token-auth/',
			data: details,
			success: function(data){
				localStorage.setItem('token',data.token);
				new $.nd2Toast({
                    message : data.token,
                    ttl : 3000
                });
                $.mobile.changePage('http://atcserver.herokuapp.com/#innovators_page');
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Log in failed: ',
                    ttl : 3000
                });
			}
		});

	});

	$('#go_to_admin').click(function(e){
		e.preventDefault();
		if (localStorage.getItem('token')===null){
			new $.nd2Toast({
                    message : 'Please Log in first',
                    ttl : 3000
                });
		}
		else{
			new $.nd2Toast({
                    message : 'Loading Profile',
                    ttl : 3000
                });
			$.ajax({
				type: 'GET',
				beforeSend: function(xhr){
					xhr.setRequestHeader("Authorization",'Token '+localStorage.getItem('token'));
				},
				url: 'http://atcserver.herokuapp.com/innovators/myprofile/',
				success: function(data){

					console.log('Success getting data');

					console.log(data);
					$('#pro-views').text(data.views);
					$('#my-innovator-name').text(data.innovator_name);
					$('#my-innovator-email').text(data.innovator_email);
					$('#my-innovator-location').text(data.innovator_location);
					$('#my-innovator-bio').text(data.innovator_bio_short);
					$('#my-innovator-description').text(data.innovator_bio_long);

					localStorage.setItem('currentInnovator',data.user_relation.id);

					$.mobile.changePage('index2.html#innovator_admin_page');

				},
				error: function(){
					new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });
				}
			});
		}
	});

	var get_innovators_list = function(){
		$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/innovators/',
			success: function(data){
				loadInnovatorsList(data);
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });	
			}
		});
	};

	var loadInnovatorsList = function(data){
		$('ul#my-innovator-list').empty();

		data.forEach(function(innovator){
			$('ul#my-innovator-list').append('<li ><a href="'+innovator.user_relation.id+'"><img src="img/user.png" class="ui-thumbnail ui-thumbnail-circular" /><h2>'+innovator.innovator_name+'</h2><p>'+innovator.innovator_bio_short+'</p></a></li>');		
		});

		$('ul#my-innovator-list').listview('refresh');

		$('ul#my-innovator-list li a').on('click', function(e){
			console.log('Innovator item clicked');
			e.preventDefault();
			var value = $(this).attr('href');
			console.log(value);
			openInnovatorPage(value);
		});

	}

	var openInnovatorPage = function(identifier){
		new $.nd2Toast({
                    message : 'Getting Innovator...',
                    ttl : 3000
                });
		$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/innovators/'+identifier+'/',
			success: function(data){
				console.log(data);
				$('#text-innovator-views').text(data.views);
				$('#text-innovator-name').text(data.innovator_name);
				$('#text-innovator-email').text(data.innovator_email);
				$('#text-innovator-location').text(data.innovator_location);
				$('#text-innovator-short-bio').text(data.innovator_bio_short);
				$('#text-innovator-description').text(data.innovator_bio_long);

				//used to get ideas and experience
				localStorage.setItem('currentInnovator',identifier);

				$.mobile.changePage('index2.html#innovator_page');
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });
			}
		});

	};


	$(document).on('pagebeforeshow','#innovators_page', function(){
		console.log('Innovators page being opened');
		get_innovators_list();
	});

	var getIdeasList = function(){
		console.log('getList token: '+localStorage.getItem('token'));
		if (localStorage.getItem('token')===null){
			$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/ideas/',
			success: function(data){
				loadIdeasList(data);
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });	
			}
		});
		}
		else{
			$.ajax({
			type: 'GET',
			beforeSend: function(xhr){
				xhr.setRequestHeader("Authorization",'Token '+localStorage.getItem('token'));
			},
			url: 'http://atcserver.herokuapp.com/ideas/',
			success: function(data){
				loadIdeasList(data);
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });	
			}
		});	
		}
		
	};

	var loadIdeasList = function(data){
		console.log(data);
		console.log('load ideas list function called');
		$('ul#my-ideas-list').empty();

		data.forEach(function(idea){
			console.log(idea);
			$('ul#my-ideas-list').append('<li><a href="'+idea.identifier+'"><h2>'+idea.idea_name+'</h2><p>'+idea.idea_bio_short+'</p></a></li>');	
		});

		$('ul#my-ideas-list').listview('refresh');

		$('#my-ideas-list li a').on('click',function(e){
			e.preventDefault();
			var value = $(this).attr('href');
			console.log(value);
			openIdeaView(value);
		});

	}

	var openIdeaView= function(identifier){
		console.log('Identifier: '+identifier);
		new $.nd2Toast({
            message : 'Getting Idea...',
            ttl : 3000
            });
		if (localStorage.getItem('token')===null){
			$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/ideas/'+identifier+'/',
			success: function(data){
				console.log(data.identifier);
				console.log(data.idea_name);
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });	
			}
		});
		}else{
			$.ajax({
			type: 'GET',
			beforeSend: function(xhr){
				xhr.setRequestHeader("Authorization",'Token '+localStorage.getItem('token'));
			},
			url: 'http://atcserver.herokuapp.com/ideas/'+identifier+'/',
			success: function(data){
				console.log(data.identifier);
				console.log(data.idea_name);
			},
			error: function(){
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });	
			}
		});	
		}
	
	};

	$(document).on('pagebeforeshow','#ideas_page', function(){
		console.log('Ideas page opened.');
		getIdeasList();
	});

	$('#send-experience').click(function(event) {
		
		var details = {
			start_date : null,
			end_date : null,
			description : null,
			skills_learnt : null
		};

		details.start_date = $('#exp-start').val();
		details.end_date = $('#exp-end').val();
		details.description = $('#exp-description').val();
		details.skills_learnt = $('#exp-skills').val()

		$.ajax({
			type:'POST',
			beforeSend: function(xhr){
				xhr.setRequestHeader("Authorization",'Token '+localStorage.getItem('token'));
			},
			url: 'http://atcserver.herokuapp.com/experiences/add/',
			data: details,
			success: function(data){
				new $.nd2Toast({
                    message : 'Added a new experience to your profile',
                    ttl : 3000
                });	
			},
			error: function(e){
				console.log(e);
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });
			}

		});

		console.log(details);

	});

	$('#idea-add-button').click(function(event) {
		var details = {
			idea_name : null,
			idea_bio_short : null,
			idea_bio_long : null,
			category : null,
			is_public : null
		};

		if ($('#is-public option:selected').text()=='No'){
			details.is_public = true;
		}
		else{
			details.is_public = false;
		}
		
		details.category = $('#select-category option:selected').text();

		details.idea_name = $('#idea_name_input').val();
		details.idea_bio_short = $('#idea_bio_short_input').val();
		details.idea_bio_long = $('#idea_bio_long_input').val();

		console.log(details);

		$.ajax({
			type: 'POST',
			beforeSend: function(xhr){
				xhr.setRequestHeader("Authorization",'Token '+localStorage.getItem('token'));
			},
			data: details,
			url: 'http://atcserver.herokuapp.com/ideas/post/',
			success: function(data){
				new $.nd2Toast({
                    message : 'Added a new idea to your profile',
                    ttl : 3000
                });
			},
			error: function(data){
				console.log(data);
				new $.nd2Toast({
                    message : 'Server returned an error',
                    ttl : 3000
                });	
			}
		});

	});

	$('#go-to-become-inno').click(function(event) {

		event.preventDefault();

		console.log('token: '+localStorage.getItem('token'));

		if(localStorage.getItem('token')===null){
			new $.nd2Toast({
                    message : 'Please log in to your account',
                    ttl : 3000
                });
			return;
		}

		$.mobile.changePage('index2.html#innovator_signup_page');

	});

	$('#innovator_signup_request').click(function(){

		var details = {
			innovator_name : null,
			innovator_email : null,
			innovator_bio_short : null,
			innovator_bio_long :  null,
			innovator_location : null,
		};

		details.innovator_name = $('#innovator_name_input').val();
		details.innovator_email = $('#innovator_email_input').val();
		details.innovator_bio_short = $('#innovator_short_bio_input').val();
		details.innovator_bio_long = $('#innovator_long_bio_input').val();
		details.innovator_location = $('#innovator_location_input').val();

		console.log(details);

		$.ajax({
			type: 'POST',
			beforeSend: function(xhr){
				xhr.setRequestHeader("Authorization",'Token '+localStorage.getItem('token'));
			},
			data: details,
			url: 'http://atcserver.herokuapp.com/innovators/create/',
			success: function(data){
				new $.nd2Toast({
                    message : 'Created Innovator Account',
                    ttl : 3000
                });
                $.mobile.changePage('index2.html#')
			},
			error: function(data){
				console.log(data);
				new $.nd2Toast({
                    message : 'Server returned an errror message',
                    ttl : 3000
                });
			}
		});

	});

	var getExperiencesAdmin = function(){
		$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/experiences/'+localStorage.getItem('currentInnovator')+'/',
			success: function(data){
				loadExperiencesAdmin(data);
			},
			error: function(data){
				console.log(data);
				new $.nd2Toast({
                    message : 'Server returned an errror message',
                    ttl : 3000
                });
			}
		});
	};

	var loadExperiencesAdmin = function(data){

		$('ul#my-exp-admin-list').empty();

		data.forEach(function(experience){
			$('ul#my-exp-admin-list').append('<li><a href="#"><h2>Skills learnt</h2><p>'+experience.skills_learnt+'</p></a></li>');		
		});

		$('ul#my-exp-admin-list').listview('refresh');

	};

	$(document).on('pagebeforeshow','#experience_page_admin', function(){
		console.log('Admin experiences opened.');
		getExperiencesAdmin();
	});

	var getExperiences = function(){
		$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/experiences/'+localStorage.getItem('currentInnovator')+'/',
			success: function(data){
				loadExperiences(data);
			},
			error: function(data){
				console.log(data);
				new $.nd2Toast({
                    message : 'Server returned an errror message',
                    ttl : 3000
                });
			}
		});
	};

	var loadExperiences = function(data){

		$('ul#my-exp-list').empty();

		data.forEach(function(experience){
			$('ul#my-exp-list').append('<li><a href="#"><h2>Skills learnt</h2><p>'+experience.skills_learnt+'</p></a></li>');		
		});

		$('ul#my-exp-list').listview('refresh');

	};

	$(document).on('pagebeforeshow','#experience_page', function(){
		console.log('Normal experiences opened.');
		getExperiences();
	});




	$('#find-inn').click(function(){
		console.log('Trying to find innovators');

		var keyword = $('#search-criteria').val();

		$('ul#my-results-list').empty();

		$.ajax({
			type: 'GET',
			url: 'http://atcserver.herokuapp.com/innovators/'+keyword+'/keyword/',
			success: function(data){
				
				data.forEach(function(innovator){
					$('ul#my-results-list').append('<li ><a href="'+innovator.user_relation.id+'"><img src="img/user.png" class="ui-thumbnail ui-thumbnail-circular" /><h2>'+innovator.innovator_name+'</h2><p>'+innovator.innovator_bio_short+'</p></a></li>');					
				});

				$('ul#my-results-list').listview('refresh');

			},
			error: function(data){
				console.log(data);
				
			}
		});

	});
















});
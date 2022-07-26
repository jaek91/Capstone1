let FAV_URL = '/users/favorites/add';
let TOWATCH_URL = '/users/towatch/add';
let WATCHED_URL = '/users/watched/add';

//helper function to extract only the integer part to the fav id from del button
function getId(str) {
    let num = str.replace(/[^0-9]/g, '');
    return parseInt(num,10)
}

$(document).ready( function() { 

    //--------------------------------------------------------------------//
    //----------HANDLE ALL ADDING TO FAV/TOWATCH/WATCHED LIST-------------//
    //--------------------------------------------------------------------//

    for (let i = 0; i < 3; i++) { 

        let favButton = $(`#add_to_favorites-${i}`)
        let disablefavButtonData = favButton.data('disable')
        
        if (disablefavButtonData) {
            favButton.addClass("disabled");
            favButton.text("In Favorites!")
        }

        let toWatchButton = $(`#add_to_watch-${i}`)
        let disabletoWatchButtonData = toWatchButton.data('disable')
        
        if (disabletoWatchButtonData) {
            toWatchButton.addClass("disabled");
            toWatchButton.text("In To-Watch!")
        }

        let watchedButton = $(`#add_to_watched-${i}`)
        let disablewatchedButtonData = watchedButton.data('disable')
        
        if (disablewatchedButtonData) {
            watchedButton.addClass("disabled");
            watchedButton.text("In Watched!")
        }
        //-----handle favorites adding------//
        $(`#add_to_favorites-${i}`).on('click', function(event){
            event.preventDefault();
            
            const $categoryButton = $(this)
            
            let id = $categoryButton.closest('.anime_container').find('h2.anime_title').attr('id')
            let anime_title = $categoryButton.closest('.anime_container').find('h2.anime_title').html()

            let selectedBool = $categoryButton.data('selected', 'true')
            if (selectedBool) {
                $(this).prop("disabled", true);
            }
            
            $.ajax({
                url: FAV_URL,
                type: "POST",
                data: JSON.stringify({'id': id}),
                dataType: "text",
                contentType: "application/json",
                success: function() {
                        $("#fav-success").append(`<b><p class="text-light bg-success"> ${anime_title} was successfully added to the favorites list!</p></b>`)
                        console.log("data was sent successfully to the favorites list!")
                },
                error: function(error){
                    console.log('something wrong happened while trying to add to the favorites list', error);
                }
                });
            })

        //-----handle to watch adding------//
        $(`#add_to_watch-${i}`).on('click', function(event){
            event.preventDefault();
            
            const $categoryButton = $(this)
            
            let id = $categoryButton.closest('.anime_container').find('h2.anime_title').attr('id')
            let anime_title = $categoryButton.closest('.anime_container').find('h2.anime_title').html()
            
            let selectedBool = $categoryButton.data('selected', 'true')

            if (selectedBool) {
                $(this).prop("disabled", true);
            }
            
            $.ajax({
                url: TOWATCH_URL,
                type: "POST",
                data: JSON.stringify({'id': id}),
                dataType: "text",
                contentType: "application/json",
                success: function() {
                    $("#towatch-success").append(`<b><p class="text-light bg-success">${anime_title} was successfully added to the to-watch list!</p></b>`)
                    console.log("data was sent successfully to the to_watch list!")
                },
                error: function(error) {
                    console.log('something wrong happened while trying to add to the to-watch list', error)
                }
                });
            })
            
        //-----handle watched adding------//
        $(`#add_to_watched-${i}`).on('click', function(event){
            event.preventDefault();
            
            const $categoryButton = $(this)
            
            let id = $categoryButton.closest('.anime_container').find('h2.anime_title').attr('id')
            let anime_title = $categoryButton.closest('.anime_container').find('h2.anime_title').html()
            let selectedBool = $categoryButton.data('selected', 'true')
            if (selectedBool) {
                $(this).prop("disabled", true);
            }
    
            $.ajax({
                url: WATCHED_URL,
                type: "POST",
                data: JSON.stringify({'id': id}),
                dataType: "text",
                contentType: "application/json",
                success: function() {
                    $("#watched-success").append(`<b><p class="text-light bg-success">${anime_title} was successfully added to the watched list!</p></b>`)
                    console.log("data was sent successfully to the watched list!")
                },
                error: function(error) {
                    console.log('something wrong happened while trying to add to the to watched list', error)
                }
                });
            })
    }

    //-----------------------------------------------//
    //----------HANDLE ALL DELETE ROUTES-------------//
    //-----------------------------------------------//
    for (let i = 1; i < 100; i++) {

        $(`#delete_fav-${i}`).on('click', function(event){
            event.preventDefault();
            const $deleteButton = $(this);
    
            let anime_title = $deleteButton.parent().find('h2.anime_title').text()
            let id = $deleteButton.attr('id')
            let fav_id = getId(id)
            console.log(`${fav_id} is the id of the anime to be sent in the request`)
    
            let username = $deleteButton.parent().data('username')
    
            let FAV_DEL_URL = `/users/${username}/favorites/delete`;
    
            let selectedBool = $deleteButton.data('selected', 'true')
            if (selectedBool) {
                $deleteButton.prop("disabled", true)
            }
            
            $.ajax({
                url: FAV_DEL_URL,
                type: "POST",
                data: JSON.stringify({'title': anime_title, 'id': fav_id}),
                dataType: "text",
                contentType: "application/json",
                success: function() {   
                        window.location.replace(`/users/${username}/favorites`);
                        console.log("fav data was sent to be deleted!");
                    }
               });
            })
            
        $(`#delete_watched-${i}`).on('click', function(event){
            event.preventDefault();
            const $deleteButton = $(this);
    
            let anime_title = $deleteButton.parent().find('h2.anime_title').text()
            let id = $deleteButton.attr('id')
            let watched_id = getId(id)
    
            console.log(`${watched_id} is the id of the anime to be sent in the request`)
    
            let username = $deleteButton.parent().data('username')
    
            let WATCHED_DEL_URL = `/users/${username}/watched/delete`;
    
            let selectedBool = $deleteButton.data('selected', 'true')
            if (selectedBool) {
                $deleteButton.prop("disabled", true)
            }
            
            $.ajax({
                url: WATCHED_DEL_URL,
                type: "POST",
                data: JSON.stringify({'title': anime_title, 'id': watched_id}),
                dataType: "text",
                contentType: "application/json",
                success: function() {   
                        window.location.replace(`/users/${username}/watched`);
                        console.log("watched anime data was sent successfully to be deleted!")
                    },
                });
            })
    
        $(`#delete_to_watch-${i}`).on('click', function(event){
            event.preventDefault();
            const $deleteButton = $(this);
    
            let anime_title = $deleteButton.parent().find('h2.anime_title').text()
            let id = $deleteButton.attr('id')
            let towatch_id = getId(id)
            console.log(`${towatch_id} is the id of the anime to be sent in the request`)
    
            let username = $deleteButton.parent().data('username')
    
            let TOWATCH_DEL_URL = `/users/${username}/towatch/delete`;
    
            let selectedBool = $deleteButton.data('selected', 'true')
            if (selectedBool) {
                $deleteButton.prop("disabled", true)
            }
            
            $.ajax({
                url: TOWATCH_DEL_URL,
                type: "POST",
                data: JSON.stringify({'title': anime_title, 'id': towatch_id}),
                dataType: "text",
                contentType: "application/json",
                success: function() {   
                        window.location.replace(`/users/${username}/towatch`);
                        // $("#delete-towatch").append(`<p class="text-success">${anime_title} was successfully deleted from the to-watch list!</p>`)
                        console.log("to watch anime data was sent successfully to be deleted!")
                    },
                });
            })

        }
 
})






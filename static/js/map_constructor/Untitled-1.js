// ======================================================================================
// MARKER
// ** map need exist in this scope
// ======================================================================================
var marker_selected = false
var marker_selected_one_ago = false
function select_marker(marker){
    if(marker_selected){
        $(marker_selected.marker._icon).css('filter', '');
        if(marker_selected === marker){
            marker_selected_one_ago = marker_selected
            marker_selected = false;
            return
        }
    } 
    marker_selected_one_ago = marker_selected
    marker_selected = marker;
    $(marker_selected.marker._icon).css('filter', 'hue-rotate(280deg)');
}

class Marker {
    constructor(lat, lng, color="blue", onclick_function=false) {
        this.lat = lat;
        this.lng = lng;
        this.color = color;
        this.marker = false;
        this.onclick_function = onclick_function;
        this.set_marker();
        this.set_onclick_function();
    };
    set_marker(){
        this.marker = L.marker([this.lat, this.lng]).addTo(map);
    };
    get_coords(){
        return [this.lat, this.lng]
    }
    set_onclick_function(){
        if(!this.onclick_function){
            let self = this;
            this.marker.on('click', function(e){
                console.log(self);
                select_marker(self);
            });
        } else{
            this.marker.on('click', this.onclick_function);
        };
    };
}
function make_point_action(e){
    let marker = new Marker(e.latlng.lat, e.latlng.lng)
    select_marker(marker);
    return marker
};
make_point_action.on = false
make_point_action.off = false
// ======================================================================================
// LINHA
// ** map need exist in this scope
// ======================================================================================
class Line {
    constructor(color='red') {
        this.color = color
        this.polyline = false
        this.initial_marker = false
        this.final_marker = false
    };
    check_if_itself(marker){
        if(marker == this.initial_marker | marker == this.final_marker){
            return true
        } else{
            return false
        }
    }
    make_line(e) {
        if(!this.final_marker){
            if(!marker_selected){
                if(!this.initial_marker){
                    this.initial_marker = new Marker(e.latlng.lat, e.latlng.lng)
                    select_marker(this.initial_marker)
                }
            } else {
                if(marker_selected_one_ago != false){
                    this.initial_marker = marker_selected_one_ago;
                    this.final_marker =  marker_selected
                } else{
                    this.initial_marker = marker_selected
                    this.final_marker = new Marker(e.latlng.lat, e.latlng.lng)
                    select_marker(this.final_marker)
                }                
            }
        }
        if(this.final_marker){
            this.update_polyline()
        }
    };
    update_polyline(){
        if(this.polyline){map.removeLayer(this.polyline)};
        this.polyline = L.polyline(
            [
                this.final_marker.get_coords(),
                this.initial_marker.get_coords()
            ], 
            {color:this.color}
        ).addTo(map);
    };
};   
var line = false
function make_line_action(e){
    line.make_line(e);
};
function on_make_line_action(){
    line = new Line(); 
}
function off_make_line_action(){
    line = false;
}
make_line_action.on = on_make_line_action
make_line_action.off = off_make_line_action
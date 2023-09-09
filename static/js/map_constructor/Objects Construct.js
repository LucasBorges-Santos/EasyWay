// ======================================================================================
// MARKER
// ** map need exist in this scope
// ======================================================================================
var marker_selected = false;
var marker_selected_one_ago = false;
var marker_to_marker = false;

function select_marker(marker){
    if(marker_selected){
        $(marker_selected.marker._icon).css('filter', '');
        if(marker_selected === marker){
            marker_selected = false;
            marker_to_marker = false;
            return
        } else{
            marker_to_marker = true;
            marker_selected_one_ago = marker_selected;
            marker_selected = marker;
            $(marker_selected.marker._icon).css('filter', 'hue-rotate(280deg)'); 
        }
    } else{
        marker_to_marker = false;
        marker_selected = marker;
        $(marker_selected.marker._icon).css('filter', 'hue-rotate(280deg)');
    }
}

class Marker {
    constructor(lat, lng, color="blue") {
        this.lat = lat;
        this.lng = lng;
        this.color = color;
        this.marker = false;
        this.set_marker();
        this.set_onclick_function();
    };
    set_marker(){
        this.marker = L.marker([this.lat, this.lng]).addTo(map);
        this.marker.map_object = this;
    };
    get_coords(){
        return [this.lat, this.lng]
    }
    set_onclick_function(){
        this.marker.on('click', get_clicked_object)

        // if(!this.onclick_function){
        //     let self = this;
        //     this.marker.on('click', function(e){
        //         select_marker(self);
        //     });
        // } else{
        //     this.marker.on('click', this.onclick_function);
        // };
    };
}
function make_point_action(self, e){
    console.log(e)
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
        this.color = color;
        this.polyline = false;
        this.initial_marker = false;
        this.final_marker = false;
        this.set_initial_point();
    };
    check_if_itself(marker){
        if(marker == this.initial_marker | marker == this.final_marker){
            return true
        } else{
            return false
        }
    }
    set_initial_point(){
        if(marker_selected){
            this.initial_marker = marker_selected;
        }
    }
    make_line(self, param) {
        if(!self.initial_marker){
            if(param instanceof Marker){
                self.initial_marker = param;
            } else {
                self.initial_marker = new Marker(param.latlng.lat, param.latlng.lng);
            }
            select_marker(self.initial_marker);
        } else if(!self.final_marker){
            if(param instanceof Marker){
                self.final_marker = param;
            } else {
                self.final_marker = new Marker(param.latlng.lat, param.latlng.lng);
            }
            select_marker(self.final_marker);
        }
        if(self.final_marker){
            self.update_polyline(self)
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
function make_line_action(line, e){
    line.make_line(line, e)
    // line.make_line(e);
};
function on_make_line_action(){
    line = new Line(); 
}
function off_make_line_action(){
    line = false;
}
make_line_action.on = on_make_line_action
make_line_action.off = off_make_line_action

// ======================================================================================
// MAP General Function
// ** map need exist in this scope
// ======================================================================================
var active_function = false;
function get_clicked_object(e){
    let param = false;
    if(this.map_object instanceof Marker){
        param = this.map_object;
        select_marker(param);
    } else{
        param = e;
    };
    if(active_function){
        active_function(line, param);
    };
}
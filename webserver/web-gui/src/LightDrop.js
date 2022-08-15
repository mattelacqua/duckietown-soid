// Import React
import React from "react";

// Import Multiselect 
import Multiselect from 'multiselect-react-dropdown';

// Import io from socket to send to backend flask
import io from 'socket.io-client';

// Create the socket
const socket = io();

// Component for AngleDial (rendered from Agent)
class LightDrop extends React.Component {

  
  // Dial has a cur_angle and an id
  constructor(props) {
    super(props);
    const lights = this.props.lights;
    const already_on = lights.filter(light => light.on);
    this.state = {
        agent_id: this.props.agent_id,
        lights: lights,
        selectedValues: already_on
    };
    this.onSelect = this.onSelect.bind(this);
    this.onRemove = this.onRemove.bind(this);
  }

  
  // When we select one we need to update parent and emit change to socket:
  onSelect(selectedList, selectedItem) {
    // Instantiate var with selected 
    const turn_on = selectedItem;

    // Set it to be on
    turn_on.on = true;

    // Pass update change through parent function
    this.props.lights_pass(turn_on);

    // Get the updated list of lights and emit to socket
    const old_lights = this.state.lights;
    const new_lights = [turn_on];
    const updated = old_lights.map(obj => new_lights.find(o=> o.light === obj.light) || obj);
    socket.emit('lights',
                    {
                      'id':this.state.agent_id,
                      'lights':updated
                    });
  }

  // Same as onSelect but for removing
  onRemove(selectedList, removedItem) {
    const turn_off = removedItem;
    turn_off.on = false;
    this.props.lights_pass(turn_off);
    
    // Get the updated list of lights and emit to socket
    const old_lights = this.state.lights;
    const new_lights = [turn_off];
    const updated = old_lights.map(obj => new_lights.find(o=> o.light === obj.light) || obj);
    socket.emit('lights',
                    {
                      'id':this.state.agent_id,
                      'lights':updated
                    });}
  
  // Render the Dial component from the react-dial-knob package
  render() {
    return ( 
      <div>
        <Multiselect

          options={this.state.lights} // Options to display in the dropdown
          selectedValues={this.state.selectedValues} // Preselected value to persist in dropdown
          onSelect={this.onSelect} // Function will trigger on select event
          onRemove={this.onRemove} // Function will trigger on remove event
          displayValue="light" // Property name to display in the dropdown options
          avoidHighlightFirstOption // Property name to display in the dropdown options
          />
      </div>)
    } // End Render
} // End Class





// Let us use in other componenets
export default LightDrop;

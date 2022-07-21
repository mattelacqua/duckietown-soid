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
    console.log("Prop Lights");
    console.log(lights);
    console.log(this.props.lights);
    const already_on = lights.filter(light => light.on);
    console.log("already on");
    console.log(already_on);
    this.state = {
        agent_id: this.props.agent_id,
        lights: lights,
        selectedValues: already_on
    };
    this.onSelect = this.onSelect.bind(this);
    this.onRemove = this.onRemove.bind(this);
  }

  
  onSelect(selectedList, selectedItem) {
    console.log("Selected List");
    console.log(selectedList);
    console.log("Selected Item");
    console.log(selectedItem);
    // New light
  }

  onRemove(selectedList, removedItem) {
    console.log("Selected List");
    console.log(selectedList);
    console.log("Removed Item");
    console.log(removedItem);
  }
  
  // Render the Dial component from the react-dial-knob package
  render() {
    console.log("VALUES IN RENDER");
    console.log(this.state.selectedValues);
    return ( 
      <Multiselect
        options={this.state.lights} // Options to display in the dropdown
        selectedValues={this.state.selectedValues} // Preselected value to persist in dropdown
        onSelect={this.onSelect} // Function will trigger on select event
        onRemove={this.onRemove} // Function will trigger on remove event
        displayValue="light" // Property name to display in the dropdown options
        avoidHighlightFirstOption // Property name to display in the dropdown options
        />);
    } // End Render
} // End Class





// Let us use in other componenets
export default LightDrop;

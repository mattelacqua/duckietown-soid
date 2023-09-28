import React from "react";

// Import Multiselect 
import Multiselect from 'multiselect-react-dropdown';

import './Counterfactuals.css'


// Component to spit out agent information
class MultiDirection extends React.Component {

    // Dial has a cur_angle and an id
    constructor(props) {
      super(props);
      let directions = [
        {'direction': 'right',
         'selected': false},
        {'direction': 'left',
         'selected': false},
        {'direction': 'straight',
         'selected': false},
      ]

      const already_selected = directions.filter(direction => direction.selected);
      this.state = {
          agent_id: this.props.agent_id,
          directions: directions,
          selectedValues: already_selected
      };
      this.onSelect = this.onSelect.bind(this);
      this.onRemove = this.onRemove.bind(this);
    }
  
    
    // When we select one we need to update parent and emit change to socket:
    onSelect(selectedList, selectedItem) {
      // Instantiate var with selected 
      const selection = selectedItem;
  
      // Set it to be on
      selection.selected = true;
  
      // Get the updated list of directions
      const old_directions = this.state.directions;
      const new_directions = [selection];
      const updated = old_directions.map(obj => new_directions.find(o=> o.direction === obj.direction) || obj);
      this.setState({
        directions: updated,
      })
      // Callback to set in right state
      this.props.set_multi_direction(updated);
   }
  
    // Same as onSelect but for removing
    onRemove(selectedList, removedItem) {
      const to_remove = removedItem;
      to_remove.selected = false;
      
      // Get the updated list of lights and emit to socket
      const old_directions = this.state.directions;
      const new_directions = [to_remove];
      const updated = old_directions.map(obj => new_directions.find(o=> o.direction === obj.direction) || obj);
      this.setState({
        directions: updated,
      })
      // Callback to set in right state
      this.props.set_multi_direction(updated);
    }
    
  render() {
    return (
      <>
        <p>including</p>
        <div className="CounterfactualMulti">
          <Multiselect
            options={this.state.directions} // Options to display in the dropdown
            selectedValues={this.state.selectedValues} // Preselected value to persist in dropdown
            onSelect={this.onSelect} // Function will trigger on select event
            onRemove={this.onRemove} // Function will trigger on remove event
            style={{chips: {background: "#999933"}}}
            closeIcon="close"
            displayValue="direction" // Property name to display in the dropdown options
            avoidHighlightFirstOption // Property name to display in the dropdown options
          />
        </div>
      </>
    )
  } // End Render
}


export default MultiDirection;

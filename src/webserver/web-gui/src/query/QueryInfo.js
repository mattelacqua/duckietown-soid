import React from "react";

import ReactTextCollapse from 'react-text-collapse';


// Component to spit out agent information
class AgentInfo extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the information to screen
  render() {
    const color = this.props.color;
    const collapse_options = {
        collapse: true,
        collapseText: '<--- show more --->',
        expandText: '--> show less <---',
        minHeight: 50,
        maxHeight: 150,
        textStyle: {
          color: color,
          padding: '10px',
          fontWeight: 'normal',
        },
      };

    let counterfactual = this.props.counterfactual;
    
    // Get the values first
    let values;
    if (counterfactual.is_value){
      values = "Value:" + counterfactual.value.toString();
    }
    else if (counterfactual.is_range){
      let operator;
      if (counterfactual.range.is_gt){
        operator = ">"
      }
      else if (counterfactual.range.is_lt){
        operator = "<"
      }
      else if (counterfactual.range.is_gte){
        operator = ">="
      }
      else if (counterfactual.range.is_lte){
        operator = "<="
      }
      values = counterfactual.range.low_bound.toString() + " " + operator + " " + counterfactual.range.high_bound.toString();
    }   

    let cf;
    if (counterfactual.is_pos_x){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: x position" {"\n"}
            "Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_pos_z){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: z position" {"\n"}
            "Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_angle){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: agnel" {"\n"}
            "Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_forward_step){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: forward step" {"\n"}
            "Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_speed){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: speed" {"\n"}
            "Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_signal_choice){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: signal_choice" {"\n"}
            "Values: " {counterfactual.range.turn_choices} {"\n"}
            </p>
    }
    else if (counterfactual.is_turn_choice){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Type: turn_choice" {"\n"}
            "Values: " {counterfactual.range.turn_choices} {"\n"}
            </p>
    }


    return (
      <div>
        {cf}
      </div>
    );
  }
}

export default AgentInfo;

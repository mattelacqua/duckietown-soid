import React from "react";

// Component to spit out agent information
class CounterfactualInfo extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the information to screen
  render() {
    const color = this.props.color;
    let counterfactual = this.props.counterfactual;
    
    // Get the values first
    let values;
    if (counterfactual.is_value){
      values = "Value:" + counterfactual.value.toString();
    }
    else if (counterfactual.is_range){
      values = counterfactual.range.low_bound.toString() + " to  " + counterfactual.range.high_bound.toString();
    }   

    let cf;
    if (counterfactual.is_pos_x){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: x-position" {"\n"}
            "Possible Possible Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_pos_z){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: z-position" {"\n"}
            "Possible Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_angle){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: angle" {"\n"}
            "Possible Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_forward_step){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: forward-step" {"\n"}
            "Possible Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_speed){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: speed" {"\n"}
            "Possible Values: " {values} {"\n"}
            </p>
    }
    else if (counterfactual.is_signalchoice){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: signal-choice" {"\n"}
            "Possible Values: " {counterfactual.range.turn_choices} {"\n"}
            </p>
    }
    else if (counterfactual.is_turnchoice){
      cf = <p style={{
                    color: color,
                    textAlign: 'left',
                    whiteSpace: 'pre-line',
            }}> 
            "Counterfactual Type: turn-choice" {"\n"}
            "Possible Values: " {counterfactual.range.turn_choices} {"\n"}
            </p>
    }


    console.log("RENDERING NOTHING");
    return (
      <div>
        {cf}
      </div>
    );
  }
}

export default CounterfactualInfo;

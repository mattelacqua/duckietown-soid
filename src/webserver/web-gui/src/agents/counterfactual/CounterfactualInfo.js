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
      values = [ counterfactual.value ];
    }
    else if (counterfactual.is_range){
      values = [ counterfactual.range.low_bound, counterfactual.range.high_bound ];
    }   

    let cf;
    if (counterfactual.is_pos_x && values.length === 1){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             <b>x pos</b> is {values[0]}
            </p>
    }
    else if (counterfactual.is_pos_x){
      console.log(values)
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             {values[0]} &le; <b>x pos</b> &le; {values[1]}
            </p>
    }
    else if (counterfactual.is_pos_z && values.length === 1){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             <b>y pos</b> is {values[0]}
            </p>
    }
    else if (counterfactual.is_pos_z){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             {values[0]} &le; <b>y pos</b> &le; {values[1]}
            </p>
    }
    else if (counterfactual.is_angle && values.length === 1){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             <b>angle</b> is {values[0]}
            </p>
    }
    else if (counterfactual.is_angle){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             {values[0]} &le; <b>angle</b> &le; {values[1]}
            </p>
    }
    else if (counterfactual.is_forward_step && values.length === 1){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             <b>forward step</b> is {values[0]}
            </p>
    }
    else if (counterfactual.is_forward_step){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             {values[0]} &le; <b>forward step</b> &le; {values[1]}
            </p>
    }
    else if (counterfactual.is_speed && values.length === 1){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             <b>speed</b> is {values[0]}
            </p>
    }
    else if (counterfactual.is_speed){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             {values[0]} &le; <b>speed</b> &le; {values[1]}
            </p>
    }
    else if (counterfactual.is_signalchoice && counterfactual.is_range){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}>
             <b>signal</b> in &#123; <i>{counterfactual.range.turn_choices.join('  ')}</i> &#125;
            </p>
    }
     else if (counterfactual.is_signalchoice){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}> 
             <b>signal</b> is <i>{counterfactual.value.toLowerCase()}</i>
           </p>
    }
    else if (counterfactual.is_turnchoice && counterfactual.is_range){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}> 
             <b>turn choice</b> in &#123; <i>{counterfactual.range.turn_choices.join('  ')}</i> &#125;
           </p>
    }
    else if (counterfactual.is_turnchoice){
      cf = <p style={{
                color: color,
                textAlign: 'left',
                fontWeight: 'normal',
                whiteSpace: 'pre-line',
              }}> 
             <b>turn choice</b> is <i>{counterfactual.value.toLowerCase()}</i>
           </p>
    }
    return (
      <div>
        {cf}
      </div>
    );
  }
}

export default CounterfactualInfo;

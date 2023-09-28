// Import React
import React from "react";

// Agent Component (gets rendered in app)
class CounterfactualRange extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      low_bound: props.default_val,
      high_bound: props.default_val,
    };
    this.props.set_bound(props.default_val, "low");
    this.props.set_bound(props.default_val, "high");
  }

  // Render the agent component 
  render() {

    let lp = "low, current value is ".concat(this.state.low_bound.toString());
    let hp = "high, current value is ".concat(this.state.high_bound.toString())

    return (
      <>
      <p>of</p>
      <div className="CounterfactualWriter">
        <form>
          <label>
            <input type="text"
                   placeholder={lp}
                   onChange = {(e) => {
                     this.setState({low_bound:e.target.value});
                     this.props.set_bound(e.target.value, "low");
                   } } />
          </label>  
        </form>
      </div>
      <p>to</p>
      <div className="CounterfactualWriter">
        <form>
          <label>
            <input type="text"
                   placeholder={hp}
                   onChange = {(e) => {
                     this.setState({high_bound:e.target.value});
                     this.props.set_bound(e.target.value, "high");
                   } } />
          </label>  
        </form>
      </div>
      </>
    );
  }
}

// Allow it to be called in other functions
export default CounterfactualRange;

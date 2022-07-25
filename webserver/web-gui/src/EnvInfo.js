import React from "react";


// Component to spit out agent information
class EnvInfo extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
      max_NS: props.max_NS,
      max_EW: props.max_EW,
      tile_size: props.tile_size,
    };
  }

  // Render the information to screen
  render() {
    return (
      <div>
          {/* HTML FOR ALL THE INFORMATION */}
          <h1> Max NS: {this.props.max_NS} </h1>
          <h1> Max EW: {this.props.max_EW} </h1>
          <h1> Tile Size: {this.props.tile_size} </h1>
      </div>
      );
    }
}


export default EnvInfo;

// Import React
import React from "react";

// Import envInfo
import EnvInfo from "./EnvInfo.js"

// Agent Component (gets rendered in app)
class Environment extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      max_NS: props.max_NS,
      max_EW: props.max_EW,
      tile_size: props.tile_size,
    };
  }

  // Render the Env component EnvInfo.js)
  render() {
    return (
              <div>
                {/* Render Environment Information */}
                <EnvInfo    max_NS={this.state.max_NS}
                            max_EW={this.state.max_EW}
                            tile_size={this.state.tile_size}/>
              </div>
          );
    }
}

// Allow it to be called in other functions
export default Environment;

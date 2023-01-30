#include "src/gym_duckietown/decision_logic/types.c"

int main(int argc, char **argv) {
  EnvironmentInfo *info = malloc(sizeof(EnvironmentInfo));
  klee_open_merge();
  info->intersection_x = { environment["intersection_x"] }, intersection_z = { environment["intersection_z"] };
  info->robot_length = { environment["robot_length"] };
  info->grid_w = { environment["grid_w"] }, grid_h = { environment["grid_h"] };
  info->road_tile_size = { environment["road_tile_size"] };
  info->max_steps = { environment["max_steps"] };
  EnvironmentAgentArray *agents = malloc(sizeof(EnvironmentAgent) * { environment["num_agents"] });
  EnvironmentAgent *agent{i} = malloc(sizeof(EnvironmentAgent));
  agent{i}->id = { agent["id"] }
  klee_make_symbolic( &agent{i}->pos_x, sizeof(float), "pos_x");
  klee_make_symbolic( &agent{i}->pos_z, sizeof(float), "pos_z");
  klee_make_symbolic( &agent{i}->angle, sizeof(float), "angle");
  klee_make_symbolic( &agent{i}->forward_step, sizeof(float), "forward_step");
  klee_make_symbolic( &agent{i}->lookahead, sizeof(float), "lookahead");
  if ({counterfactual["is_pos_x"]}){
    if ({counterfactual["is_value"]}){
      klee_assume( &agent{i}->pos_x == {counterfactual["value"]} )
    } else if ({counterfactual["is_range"]}){
      klee_assume( &agent{i}->pos_x > {counterfactual["range"]["low_bound"]} &&
      &agent{i}->pos_x < {counterfactual["range"]["high_bound"]});
    }
  }
  if ({counterfactual["is_pos_z"]}){
    if ({counterfactual["is_value"]}){
      klee_assume( &agent{i}->pos_z == {counterfactual["value"]} )
    } else if ({counterfactual["is_range"]}){
      klee_assume( &agent{i}->pos_z > {counterfactual["range"]["low_bound"]} &&
      &agent{i}->pos_z < {counterfactual["range"]["high_bound"]});
    }
  }
  if ({counterfactual["is_angle"]}){
    if ({counterfactual["is_value"]}){
      klee_assume( &agent{i}->angle == {counterfactual["value"]} )
    } else if ({counterfactual["is_range"]}){
      klee_assume( &agent{i}->angle > {counterfactual["range"]["low_bound"]} &&
      &agent{i}->angle < {counterfactual["range"]["high_bound"]});
    }
  }
  if ({counterfactual["is_forward_step"]}){
    if ({counterfactual["is_value"]}){
      klee_assume( &agent{i}->forward_step == {counterfactual["value"]} )
    } else if ({counterfactual["is_range"]}){
      klee_assume( &agent{i}->forward_step > {counterfactual["range"]["low_bound"]} &&
      &agent{i}->forward_step < {counterfactual["range"]["high_bound"]});
    }
  }
  if ({counterfactual["is_speed"]}){
    if ({counterfactual["is_value"]}){
      klee_assume( &agent{i}->speed == {counterfactual["value"]} )
    } else if ({counterfactual["is_range"]}){
      klee_assume( &agent{i}->speed > {counterfactual["range"]["low_bound"]} &&
      &agent{i}->speed < {counterfactual["range"]["high_bound"]});
    }
  }
  agents->agents_array[i] = agent{i};
  agents->num_agents += 1;
}


// if ({counterfactual["is_signalchoice"]}){
//     if ({counterfactual["is_value"]}){
//       klee_assume( &agent{i}->signal_choice == {counterfactual["value"]} )
//     } else if ({counterfactual["is_range"]}){
//       klee_assume( &agent{i}->signal_choice == {turnchoice}) //this needs to be redone
//     }
//   }
//   if ({counterfactual["is_turnchoice"]}){
//     if ({counterfactual["is_value"]}){
//       klee_assume( &agent{i}->signal_choice == {counterfactual["value"]} )
//     } else if ({counterfactual["is_range"]}){
//       klee_assume( &agent{i}->signal_choice == {turnchoice}) //this needs to be redone
//     }
//   }




//  if ({ agent["symbolic"] }[i]){
//       if ({ agent["symbolic"]["pos_x"]["is_value"] }){
//         klee_assume( &agent{i}->pos_x == { agent["symbolic"]["pos_x"]["value"] } );
//       } else if ({ agent["symbolic"]["pos_x"]["is_range"] }){
//         if ({ agent["symbolic"]["pos_x"]["range"]["is_gt"] }) {
//           if ({ agent["symbolic"]["pos_x"]["range"]["low_bound"]} != -1){
//             klee_assume( &agent{i}->pos_x > { agent["symbolic"]["pos_x"]["range"]["low_bound"] } && &agent{i}->pos_x < info->grid_w * info->road_tile_size );
//           } else {
//             klee_assume( &agent{i}->pos_x > 0 && &agent{i}->pos_x < info->grid_w * info->road_tile_size );
//           }
//         }
//         else if ({ agent["symbolic"]["pos_x"]["range"]["is_gte"] }) {
//           if ({ agent["symbolic"]["pos_x"]["range"]["low_bound"]} != -1){
//             klee_assume( &agent{i}->pos_x >= { agent["symbolic"]["pos_x"]["range"]["low_bound"] } && &agent{i}->pos_x < info->grid_w * info->road_tile_size );
//           } else {
//             klee_assume( &agent{i}->pos_x >= 0 && &agent{i}->pos_x < info->grid_w * info->road_tile_size );
//           }
//         }
//         else if ({ agent["symbolic"]["pos_x"]["range"]["is_lt"] }) {
//           if ({ agent["symbolic"]["pos_x"]["range"]["high_bound"]} != -1){
//             klee_assume( &agent{i}->pos_x < { agent["symbolic"]["pos_x"]["range"]["high_bound"] } && &agent{i}->pos_x < 0 );
//           } else {
//             klee_assume( &agent{i}->pos_x < info->grid_w * info->road_tile_size && &agent{i}->pos_x > 0 );
//           }
//         }
//         else if ({ agent["symbolic"]["pos_x"]["range"]["is_lte"] }) {
//           if ({ agent["symbolic"]["pos_x"]["range"]["high_bound"]} != -1){
//             klee_assume( &agent{i}->pos_x <= { agent["symbolic"]["pos_x"]["range"]["high_bound"] } && &agent{i}->pos_x > 0 );
//           } else {
//             klee_assume( &agent{i}->pos_x <= 0 && &agent{i}->pos_x > 0 );
//           }
//         }
//       }
//     }else{
//       klee_assume( &agent{i}->pos_x == { agent["concrete"]["pos_x"] } );
//     }
    
//     if ({ agent["symbolic"]["pos_z"]["is_pos_z"] }){
//       if ({ agent["symbolic"]["pos_z"]["is_value"] }){
//         klee_assume( &agent{i}->pos_z == { agent["symbolic"]["pos_z"]["value"] } );
//       } else if ({ agent["symbolic"]["pos_z"]["is_range"] }){
//         if ({ agent["symbolic"]["pos_z"]["range"]["is_gt"] }) {
//           if ({ agent["symbolic"]["pos_z"]["range"]["low_bound"]} != -1){
//             klee_assume( &agent{i}->pos_z > { agent["symbolic"]["pos_z"]["range"]["low_bound"] } && &agent{i}->pos_z < info->grid_h * info->road_tile_size );
//           } else {
//             klee_assume( &agent{i}->pos_z > 0 && &agent{i}->pos_z < info->grid_h * info->road_tile_size );
//           }
//         }
//         else if ({ agent["symbolic"]["pos_z"]["range"]["is_gte"] }) {
//           if ({ agent["symbolic"]["pos_z"]["range"]["low_bound"]} != -1){
//             klee_assume( &agent{i}->pos_z >= { agent["symbolic"]["pos_z"]["range"]["low_bound"] } && &agent{i}->pos_z < info->grid_h * info->road_tile_size );
//           } else {
//             klee_assume( &agent{i}->pos_z >= 0 && &agent{i}->pos_z < info->grid_h * info->road_tile_size );
//           }
//         }
//         else if ({ agent["symbolic"]["pos_z"]["range"]["is_lt"] }) {
//           if ({ agent["symbolic"]["pos_z"]["range"]["high_bound"]} != -1){
//             klee_assume( &agent{i}->pos_z < { agent["symbolic"]["pos_z"]["range"]["high_bound"] } && &agent{i}->pos_z < 0 );
//           } else {
//             klee_assume( &agent{i}->pos_z < info->grid_h * info->road_tile_size && &agent{i}->pos_z > 0 );
//           }
//         }
//         else if ({ agent["symbolic"]["pos_z"]["range"]["is_lte"] }) {
//           if ({ agent["symbolic"]["pos_z"]["range"]["high_bound"]} != -1){
//             klee_assume( &agent{i}->pos_z <= { agent["symbolic"]["pos_z"]["range"]["high_bound"] } && &agent{i}->pos_z > 0 );
//           } else {
//             klee_assume( &agent{i}->pos_z <= info->grid_h * info->road_tile_size && &agent{i}->pos_z > 0 );
//           }
//         }
//       }
//     }else{
//       klee_assume( &agent{i}->pos_z == { agent["concrete"]["pos_z"] } );
//     }
    
//     if ({ agent["symbolic"]["angle"]["isangle"] }) {
//       //to do


//     }
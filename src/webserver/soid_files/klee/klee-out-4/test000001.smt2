(set-logic ALL)
(declare-fun agent0_pos_x_ackermann!1 () (_ BitVec 32))
(declare-fun agent0_pos_z_ackermann!2 () (_ BitVec 32))
(declare-fun agent0_angle_ackermann!3 () (_ BitVec 32))
(declare-fun agent0_forward_step_ackermann!4 () (_ BitVec 32))
(declare-fun agent0_speed_ackermann!5 () (_ BitVec 32))
(declare-fun agent0_signal_choice_ackermann!7 () (_ BitVec 32))
(declare-fun agent0_turn_choice_ackermann!8 () (_ BitVec 32))
(declare-fun agent0_lookahead_ackermann!6 () (_ BitVec 32))
(declare-fun agent0_intersection_arrival_ackermann!10 () (_ BitVec 32))
(declare-fun agent0_initial_direction_ackermann!9 () (_ BitVec 32))
(declare-fun agent0_patience_ackermann!11 () (_ BitVec 32))
(declare-fun agent0_step_count_ackermann!12 () (_ BitVec 32))
(declare-fun agent1_pos_x_ackermann!32 () (_ BitVec 32))
(declare-fun agent1_pos_z_ackermann!25 () (_ BitVec 32))
(declare-fun agent1_angle_ackermann!15 () (_ BitVec 32))
(declare-fun agent1_forward_step_ackermann!40 () (_ BitVec 32))
(declare-fun agent1_speed_ackermann!26 () (_ BitVec 32))
(declare-fun agent1_turn_choice_ackermann!37 () (_ BitVec 32))
(declare-fun agent1_lookahead_ackermann!45 () (_ BitVec 32))
(declare-fun agent1_intersection_arrival_ackermann!28 () (_ BitVec 32))
(declare-fun agent1_initial_direction_ackermann!0 () (_ BitVec 32))
(declare-fun agent1_patience_ackermann!38 () (_ BitVec 32))
(declare-fun agent1_step_count_ackermann!34 () (_ BitVec 32))
(declare-fun agent1_signal_choice_ackermann!42 () (_ BitVec 32))
(declare-fun __soid__agent0_prev_pos_x_ackermann!21 () (_ BitVec 32))
(declare-fun __soid__agent0_direction_ackermann!22 () (_ BitVec 32))
(declare-fun __soid__agent0_tile_x_ackermann!41 () (_ BitVec 32))
(declare-fun __soid__agent0_tile_z_ackermann!31 () (_ BitVec 32))
(declare-fun __soid__agent0_stop_x_ackermann!43 () (_ BitVec 32))
(declare-fun __soid__agent0_stop_z_ackermann!36 () (_ BitVec 32))
(declare-fun __soid__agent1_prev_pos_x_ackermann!48 () (_ BitVec 32))
(declare-fun __soid__agent1_direction_ackermann!39 () (_ BitVec 32))
(declare-fun __soid__agent1_tile_x_ackermann!55 () (_ BitVec 32))
(declare-fun __soid__agent1_tile_z_ackermann!29 () (_ BitVec 32))
(declare-fun __soid__agent1_stop_x_ackermann!30 () (_ BitVec 32))
(declare-fun __soid__agent1_stop_z_ackermann!46 () (_ BitVec 32))
(declare-fun __soid__agent0_state_in_intersection_ackermann!53 () (_ BitVec 8))
(declare-fun __soid__agent1_state_in_intersection_ackermann!24 () (_ BitVec 8))
(declare-fun __soid__agent0_state_at_intersection_entry_ackermann!52
             ()
             (_ BitVec 8))
(declare-fun __soid__agent1_state_at_intersection_entry_ackermann!56
             ()
             (_ BitVec 8))
(declare-fun __soid__agent0_state_intersection_empty_ackermann!47
             ()
             (_ BitVec 8))
(declare-fun __soid__agent1_state_intersection_empty_ackermann!54
             ()
             (_ BitVec 8))
(declare-fun __soid__agent0_state_approaching_intersection_ackermann!16
             ()
             (_ BitVec 8))
(declare-fun __soid__agent1_state_approaching_intersection_ackermann!23
             ()
             (_ BitVec 8))
(declare-fun __soid__agent0_state_obj_in_range_ackermann!59 () (_ BitVec 8))
(declare-fun __soid__agent1_state_obj_in_range_ackermann!50 () (_ BitVec 8))
(declare-fun __soid__agent0_state_has_right_of_way_ackermann!51 () (_ BitVec 8))
(declare-fun __soid__agent1_state_has_right_of_way_ackermann!60 () (_ BitVec 8))
(declare-fun __soid__agent0_state_next_to_go_ackermann!49 () (_ BitVec 8))
(declare-fun __soid__agent1_state_next_to_go_ackermann!44 () (_ BitVec 8))
(declare-fun __soid__agent0_state_safe_to_enter_ackermann!20 () (_ BitVec 8))
(declare-fun __soid__agent1_state_safe_to_enter_ackermann!35 () (_ BitVec 8))
(declare-fun __soid__agent0_state_cars_waiting_to_enter_ackermann!33
             ()
             (_ BitVec 8))
(declare-fun __soid__agent1_state_cars_waiting_to_enter_ackermann!13
             ()
             (_ BitVec 8))
(declare-fun __soid__agent0_state_car_entering_range_ackermann!18
             ()
             (_ BitVec 8))
(declare-fun __soid__agent1_state_car_entering_range_ackermann!57
             ()
             (_ BitVec 8))
(declare-fun __soid__agent0_state_obj_behind_intersection_ackermann!14
             ()
             (_ BitVec 8))
(declare-fun __soid__agent1_state_obj_behind_intersection_ackermann!17
             ()
             (_ BitVec 8))
(declare-fun __soid__agent0_state_is_tailgating_ackermann!61 () (_ BitVec 8))
(declare-fun __soid__agent1_state_is_tailgating_ackermann!19 () (_ BitVec 8))
(declare-fun __soid__mrow__ackermann!58 () (_ BitVec 32))
(declare-fun __soid__will_proceed_ackermann!27 () (_ BitVec 8))
(assert (fp.eq ((_ to_fp 8 24) agent0_pos_x_ackermann!1) ((_ to_fp 8 24) #x3fcae148)))
(assert (fp.eq ((_ to_fp 8 24) agent0_pos_z_ackermann!2) ((_ to_fp 8 24) #x3febc6a8)))
(assert (fp.eq ((_ to_fp 8 24) agent0_angle_ackermann!3) ((_ to_fp 8 24) #x3fca9fbe)))
(assert (fp.eq ((_ to_fp 8 24) agent0_forward_step_ackermann!4)
       ((_ to_fp 8 24) #x3ee147ae)))
(assert (fp.eq ((_ to_fp 8 24) agent0_speed_ackermann!5) ((_ to_fp 8 24) #x3b03126f)))
(assert (= #x00000002 agent0_signal_choice_ackermann!7))
(assert (= #x00000002 agent0_turn_choice_ackermann!8))
(assert (fp.eq ((_ to_fp 8 24) agent0_lookahead_ackermann!6)
       ((_ to_fp 8 24) #x3f15c28f)))
(assert (= #x0000004d agent0_intersection_arrival_ackermann!10))
(assert (= #x00000000 agent0_initial_direction_ackermann!9))
(assert (= #x00000000 agent0_patience_ackermann!11))
(assert (= #x0000006c agent0_step_count_ackermann!12))
(assert (fp.eq ((_ to_fp 8 24) agent1_pos_x_ackermann!32) ((_ to_fp 8 24) #x3f92d0e5)))
(assert (fp.eq ((_ to_fp 8 24) agent1_pos_z_ackermann!25) ((_ to_fp 8 24) #x3fcb22d1)))
(assert (fp.eq ((_ to_fp 8 24) agent1_angle_ackermann!15) ((_ to_fp 8 24) #x3c8b4396)))
(assert (fp.eq ((_ to_fp 8 24) agent1_forward_step_ackermann!40)
       ((_ to_fp 8 24) #x3ee147ae)))
(assert (fp.eq ((_ to_fp 8 24) agent1_speed_ackermann!26) ((_ to_fp 8 24) #x3e2e147b)))
(assert (= #x00000002 agent1_turn_choice_ackermann!37))
(assert (fp.eq ((_ to_fp 8 24) agent1_lookahead_ackermann!45)
       ((_ to_fp 8 24) #x3f15c28f)))
(assert (= #x0000003c agent1_intersection_arrival_ackermann!28))
(assert (= #x00000002 agent1_initial_direction_ackermann!0))
(assert (= #x00000000 agent1_patience_ackermann!38))
(assert (= #x0000006c agent1_step_count_ackermann!34))
(assert (= #x00000000 agent1_signal_choice_ackermann!42))
(assert (fp.eq ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
       ((_ to_fp 8 24) __soid__agent0_prev_pos_x_ackermann!21)))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent0_angle_ackermann!3))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
         ((_ to_fp 8 24) #x42340000))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent0_angle_ackermann!3))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
          ((_ to_fp 8 24) #x43070000))))
(assert (= #x00000000 __soid__agent0_direction_ackermann!22))
(assert (= #x00000002 __soid__agent0_tile_x_ackermann!41))
(assert (= #x00000003 __soid__agent0_tile_z_ackermann!31))
(assert (fp.eq ((_ to_fp 8 24) #x3f60a3d6)
       ((_ to_fp 8 24) __soid__agent0_stop_x_ackermann!43)))
(assert (let ((a!1 (ite (fp.gt ((_ to_fp 11 53)
                         roundNearestTiesToEven
                         ((_ to_fp 8 24) agent0_speed_ackermann!5))
                       ((_ to_fp 11 53) #x3fd6666666666666))
                (fp.to_ieee_bv ((_ to_fp 8 24) #x3e99999a))
                agent0_speed_ackermann!5)))
(let ((a!2 (fp.sub roundNearestTiesToEven
                   ((_ to_fp 8 24) #x4015c28f)
                   (fp.sub roundNearestTiesToEven
                           ((_ to_fp 8 24) #x3f15c28f)
                           (fp.mul roundNearestTiesToEven
                                   ((_ to_fp 8 24) a!1)
                                   ((_ to_fp 8 24) #x3f15c28f))))))
  (fp.eq a!2 ((_ to_fp 8 24) __soid__agent0_stop_z_ackermann!36)))))
(assert (fp.eq ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
       ((_ to_fp 8 24) __soid__agent1_prev_pos_x_ackermann!48)))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent1_angle_ackermann!15))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (not (and (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                   ((_ to_fp 8 24) #x42340000))
            (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                    ((_ to_fp 8 24) #x43070000))))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent1_angle_ackermann!15))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
  (not (and (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                   ((_ to_fp 8 24) #x43070000))
            (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                    ((_ to_fp 8 24) #x43610000))))))
(assert (= #x00000002 __soid__agent1_direction_ackermann!39))
(assert (= #x00000001 __soid__agent1_tile_x_ackermann!55))
(assert (= #x00000002 __soid__agent1_tile_z_ackermann!29))
(assert (let ((a!1 (ite (fp.gt ((_ to_fp 11 53)
                         roundNearestTiesToEven
                         ((_ to_fp 8 24) agent1_speed_ackermann!26))
                       ((_ to_fp 11 53) #x3fd6666666666666))
                (fp.to_ieee_bv ((_ to_fp 8 24) #x3e99999a))
                agent1_speed_ackermann!26)))
(let ((a!2 (fp.add roundNearestTiesToEven
                   ((_ to_fp 8 24) #x3f15c28f)
                   (fp.sub roundNearestTiesToEven
                           ((_ to_fp 8 24) #x3f15c28f)
                           (fp.mul roundNearestTiesToEven
                                   ((_ to_fp 8 24) a!1)
                                   ((_ to_fp 8 24) #x3f15c28f))))))
  (fp.eq a!2 ((_ to_fp 8 24) __soid__agent1_stop_x_ackermann!30)))))
(assert (fp.eq ((_ to_fp 8 24) #x3fbb3333)
       ((_ to_fp 8 24) __soid__agent1_stop_z_ackermann!46)))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_pos_x_ackermann!1))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000002
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_in_intersection_ackermann!53) #b1)))
(assert (not (= ((_ extract 0 0) __soid__agent1_state_in_intersection_ackermann!24) #b1)))
(assert (not (fp.lt ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.lt ((_ to_fp 8 24) agent0_pos_z_ackermann!2)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.gt ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
            ((_ to_fp 8 24) #x403b3333))))
(assert (not (fp.gt ((_ to_fp 8 24) agent0_pos_z_ackermann!2)
            ((_ to_fp 8 24) #x403b3333))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_pos_z_ackermann!2))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000003
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (fp.gt ((_ to_fp 11 53)
         roundNearestTiesToEven
         ((_ to_fp 8 24) agent0_pos_z_ackermann!2))
       ((_ to_fp 11 53) #x3ffb810603333333)))
(assert (fp.lt ((_ to_fp 8 24) agent0_pos_z_ackermann!2) ((_ to_fp 8 24) #x3ff7ae14)))
(assert (= ((_ extract 0 0) __soid__agent0_state_at_intersection_entry_ackermann!52)
   #b1))
(assert (not (fp.lt ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.lt ((_ to_fp 8 24) agent1_pos_z_ackermann!25)
            ((_ to_fp 8 24) #x00000000))))
(assert (not (fp.gt ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
            ((_ to_fp 8 24) #x403b3333))))
(assert (not (fp.gt ((_ to_fp 8 24) agent1_pos_z_ackermann!25)
            ((_ to_fp 8 24) #x403b3333))))
(assert (let ((a!1 (fp.mul roundNearestTiesToEven
                   (fp.div roundNearestTiesToEven
                           ((_ to_fp 11 53)
                             roundNearestTiesToEven
                             ((_ to_fp 8 24) agent1_angle_ackermann!15))
                           ((_ to_fp 11 53) #x40091eb851eb851f))
                   ((_ to_fp 11 53) #x4066800000000000))))
(let ((a!2 (ite (and (fp.gt ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                            ((_ to_fp 8 24) #x43610000))
                     (fp.leq ((_ to_fp 8 24) roundNearestTiesToEven a!1)
                             ((_ to_fp 8 24) #x439d8000)))
                #x00000001
                #x00000002)))
  (= #x00000002 a!2))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent1_pos_x_ackermann!32))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000001
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (let ((a!1 ((_ fp.to_sbv 32)
             roundTowardZero
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent1_pos_z_ackermann!25))
                     ((_ to_fp 11 53) #x3fe2b851e0000000)))))
  (= #x00000002
     ((_ fp.to_sbv 32)
       roundTowardZero
       ((_ to_fp 11 53) roundNearestTiesToEven a!1)))))
(assert (fp.gt ((_ to_fp 8 24) agent1_pos_x_ackermann!32) ((_ to_fp 8 24) #x3f7d70a3)))
(assert (fp.lt ((_ to_fp 11 53)
         roundNearestTiesToEven
         ((_ to_fp 8 24) agent1_pos_x_ackermann!32))
       ((_ to_fp 11 53) #x3ff34bc69ccccccd)))
(assert (= ((_ extract 0 0) __soid__agent1_state_at_intersection_entry_ackermann!56)
   #b1))
(assert (= ((_ extract 0 0) __soid__agent0_state_intersection_empty_ackermann!47) #b1))
(assert (= ((_ extract 0 0) __soid__agent1_state_intersection_empty_ackermann!54) #b1))
(assert (= ((_ extract 0 0) __soid__agent0_state_approaching_intersection_ackermann!16)
   #b1))
(assert (= ((_ extract 0 0) __soid__agent1_state_approaching_intersection_ackermann!23)
   #b1))
(assert (let ((a!1 ((_ to_fp 8 24)
             roundNearestTiesToEven
             (fp.div roundNearestTiesToEven
                     ((_ to_fp 11 53)
                       roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_lookahead_ackermann!6))
                     ((_ to_fp 11 53) #x4024000000000000)))))
  (not (fp.geq ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
               (fp.sub roundNearestTiesToEven
                       ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
                       a!1)))))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_obj_in_range_ackermann!59) #b1)))
(assert (fp.geq ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
        ((_ to_fp 8 24) agent1_pos_x_ackermann!32)))
(assert (fp.leq ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
        (fp.add roundNearestTiesToEven
                ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
                ((_ to_fp 8 24) agent1_lookahead_ackermann!45))))
(assert (fp.geq ((_ to_fp 8 24) agent0_pos_z_ackermann!2)
        ((_ to_fp 8 24) agent1_pos_x_ackermann!32)))
(assert (not (fp.leq ((_ to_fp 8 24) agent0_pos_z_ackermann!2)
             (fp.add roundNearestTiesToEven
                     ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
                     ((_ to_fp 8 24) agent1_lookahead_ackermann!45)))))
(assert (not (= ((_ extract 0 0) __soid__agent1_state_obj_in_range_ackermann!50) #b1)))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_has_right_of_way_ackermann!51)
        #b1)))
(assert (= ((_ extract 0 0) __soid__agent1_state_has_right_of_way_ackermann!60) #b1))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_next_to_go_ackermann!49) #b1)))
(assert (not (= ((_ extract 0 0) __soid__agent1_state_next_to_go_ackermann!44) #b1)))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_safe_to_enter_ackermann!20) #b1)))
(assert (= ((_ extract 0 0) __soid__agent1_state_safe_to_enter_ackermann!35) #b1))
(assert (= ((_ extract 0 0) __soid__agent0_state_cars_waiting_to_enter_ackermann!33)
   #b1))
(assert (= ((_ extract 0 0) __soid__agent1_state_cars_waiting_to_enter_ackermann!13)
   #b1))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_car_entering_range_ackermann!18)
        #b1)))
(assert (not (fp.geq ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
             (fp.add roundNearestTiesToEven
                     ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
                     ((_ to_fp 8 24) agent1_lookahead_ackermann!45)))))
(assert (not (= ((_ extract 0 0) __soid__agent1_state_car_entering_range_ackermann!57)
        #b1)))
(assert (not (= ((_ extract 0 0)
          __soid__agent0_state_obj_behind_intersection_ackermann!14)
        #b1)))
(assert (fp.geq ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
        (fp.sub roundNearestTiesToEven
                (fp.sub roundNearestTiesToEven
                        ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
                        ((_ to_fp 8 24) agent1_lookahead_ackermann!45))
                ((_ to_fp 8 24) #x3e3851ec))))
(assert (not (fp.leq ((_ to_fp 8 24) agent0_pos_x_ackermann!1)
             (fp.sub roundNearestTiesToEven
                     ((_ to_fp 8 24) agent1_pos_x_ackermann!32)
                     ((_ to_fp 8 24) #x3e3851ec)))))
(assert (not (= ((_ extract 0 0)
          __soid__agent1_state_obj_behind_intersection_ackermann!17)
        #b1)))
(assert (not (= ((_ extract 0 0) __soid__agent0_state_is_tailgating_ackermann!61) #b1)))
(assert (not (= ((_ extract 0 0) __soid__agent1_state_is_tailgating_ackermann!19) #b1)))
(assert (= #x000001c8 __soid__mrow__ackermann!58))
(assert (not (= ((_ extract 0 0) __soid__will_proceed_ackermann!27) #b1)))
(check-sat)
(exit)

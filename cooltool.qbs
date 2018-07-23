import qbs

Project {
    name: "cooltool"

    MachinekitApplication {
        name: "All"
        halFiles: [
            "axis_manualtoolchange.hal",
            "axis_xy.hal",
            "axis_z.hal",
            "axis_a.hal",
            "axis_b.hal",
            "axis_c.hal",
            "base_bbb.hal",
            "base_bbb_robot.hal",
            "limit_x.hal",
            "limit_xyz_parallel.hal",
            "limit_probe_parallel.hal",
            "limit_y.hal",
            "limit_y-S4.hal",
            "limit_z.hal",
            "limit_a.hal",
            "limit_b.hal",
            "pinconfig_bbb_standard.hal",
            "pinconfig_bbb_standard-3D.hal",
            "pinconfig_bbb_standard-S4.hal",
            "pinconfig_bbb_Gravier.hal",
            "pinconfig_bbb_Unimat_sw.hal",
            "pinconfig_bbb_Unimat_sw_robot.hal",
            "pinconfig_bbb_UniStep.hal",
            "pinconfig_bbb_UniStep_H.hal",
            "spindle_pwm.hal",
            "spindle_stepgen.hal",
            "relay_spindle.hal",
            "relay_flood.hal",
            "robot_io.hal"
        ]
        configFiles: [
            "EngravingSystem_220.ini",
            "Uni-cnc-set.ini",
            "Uni-cut-2D.ini",
            "Uni-cut-3D.ini",
            "Uni-dreh.ini",
            "Uni-fraes-4.ini",
            "Uni-fraes-h3.ini",
            "Uni-fraes-v3.ini",
            "Uni-mill-cnc.ini",
            "Uni-fraes-4_sw.ini",
            "Uni-fraes-4_sc.ini",
            "Uni-fraes-4_sw_sc.ini",
            "Uni-fraes-4_sw_sc_robot.ini",
            "Uni-fraes-4_sw_sc_robot_mk.ini",
            "UniStep540-70.ini",
            "UniStep540-70_4axes.ini",
            "UniStep540-70_H.ini"
        ]
        bbioFiles: [
            "paralell_cape2.bbio",
            "paralell_cape2_p.bbio",
            "paralell_cape2_robot.bbio"
        ]
    }
}

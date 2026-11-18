---
title: "Unser Testing-Tool für ROS ist open source"
date: 2023-04-02
permalink: /2023/04/unser-testing-tool-fuer-ros-ist-open-source/
image: /assets/2023/04/ray-so-export-1360x480.png
excerpt: "Die Software die wir für die Steuerung unseres Bootes bauen ist komplex – und wie bei jedem größeren Projekt schleichen sich in der Prgrammierung unweigerlich Fehler ein. Um möglichst viele davon zu finden, testen wir unsere Software ausgiebig."
---

[Die Software]({{ site.baseurl }}/ueber-uns/team/software/) die wir für die Steuerung unseres Bootes bauen ist komplex – und wie bei jedem größeren Projekt schleichen sich in der Prgrammierung unweigerlich Fehler ein. Um möglichst viele davon zu finden, testen wir unsere Software ausgiebig.

Für die Interaktion der vielen Teilsysteme verwenden wir das [Robot Operating System (ROS)](https://www.ros.org/), wodurch es aber ein bisschen schwieriger wird die verschiedenen Systeme zu testen. Dazu haben wir intern ein Tool geschrieben, das uns dabei hilft. Es startet automatisch eine Komponente wie z.B. die Wegfindung, dann führt es den Test aus, und danach fährt es die Komponente wieder kontrolliert herunter. Und dafür braucht es nur ein paar Zeilen Code, was es uns viel einfacher macht neue Tests zu schreiben und die Übersicht über die bestehenden zu behalten.

Für alle, die gerne tatsächlichen Code sehen wollen, folgt gleich ein einfaches Beispiel. Wer möchte, kann die Bibliothek einfach herunterladen und sie selbst verwenden, siehe diese [GitHub Seite](https://github.com/SailingTeamDarmstadt/ros2-easy-test).

![from ros2_easy_test import ROS2TestEnvironment, with_single_node from near_planner import NearPlannerNode from boat_msgs.msg import PolarLocation, PolarRoute @with_single_node(NearPlannerNode, watch_topics={"/route": PolarRoute}) def test_path_finding(env: ROS2TestEnvironment) -> None: env.publish("/boat_position", PolarLocation(49.87808717, 8.65402801)) env.publish("/target_point", PolarLocation(49.87808717, 8.65402801)) target_route = env.assert_message_published("/route", timeout=10) assert len(target_route) >= 2, "Route was too short" # and more ...]({{ site.baseurl }}/assets/2023/04/ray-so-export-1536x917.png)

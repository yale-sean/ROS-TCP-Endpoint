import tf
from geometry_msgs.msg import PoseStamped
from ros_tcp_endpoint.communication import RosSender


class RosTFBroadcaster(RosSender):
    """
    Class to publish to the TF tree
    Modeled after the RosPublisher class, which takes info off the bridge and publishes to ROS
    https://github.com/Unity-Technologies/ROS-TCP-Endpoint/blob/993d366b8900bf9f3d2da444fde64c0379b4dc7c/src/ros_tcp_endpoint/publisher.py#L56
    """

    def __init__(self, child, parent):
        super().__init__(node_name=f"RosTFBroadcaster-{child}-{parent}")
        self.msg = PoseStamped()
        self.child = child
        self.parent = parent
        self.last_ts = 0

    def send(self, data):
        br = tf.TransformBroadcaster()
        self.msg.deserialize(data)
        ts = self.msg.header.stamp.to_sec()
        #print(f"got transform: {self.parent} -> {self.child}")
        if ts <= self.last_ts:
            return
        self.last_ts = ts
        p = self.msg.pose.position
        o = self.msg.pose.orientation
        br.sendTransform((p.x, p.y, p.z),
                        (o.x, o.y, o.z, o.w),
                        self.msg.header.stamp,
                        self.child,
                        self.parent)
        return None

    def unregister(self):
        pass
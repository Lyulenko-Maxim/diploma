import {Avatar, AvatarGroup, Chip, getKeyValue, User} from "@nextui-org/react";
import {CameraOff, Circle} from "lucide-react";
import React from "react";
import {IProfile} from "@/types/user.types";
import {IProjectColumn, IProjectMember, IProjectTableProps} from "@/types/project.types";
import {IGroup} from "@/types/group.types";

const renderOwnerColumn = (owner: IProfile) => {
    const {username, first_name, last_name, photo} = owner;
    return (
        <div>
            <User
                name={username}
                description={(first_name || '') + ' ' + (last_name || '')}
                avatarProps={{
                    isBordered: true,
                    src: typeof photo === 'string' ? photo : '',
                    fallback: <CameraOff/>
                }}
            />
        </div>
    );
};

const renderMembersColumn = (members: IProjectMember[], members_count: number) => {
    return (
        <div>
            <AvatarGroup isBordered max={3} total={members_count} className="justify-start">
                {members.map((member) => {
                    const {photo, id} = member.profile;
                    return <Avatar key={id} src={typeof photo === 'string' ? photo : ''}/>;
                })}
            </AvatarGroup>
        </div>
    );
};

const renderMyGroupColumn = (my_group: IGroup) => {
    const {name, color_hex} = my_group;
    return (
        <div>
            <Chip
                startContent={<Circle strokeWidth={0} size={16} fill={color_hex}/>}
                variant="faded"
                className="text-foreground"
            >
                {name}
            </Chip>
        </div>
    );
};

export const renderCells = (item: IProjectTableProps, column: IProjectColumn) => {
    switch (column.key) {
        case 'owner':
            return renderOwnerColumn(item.owner);
        case 'members':
            return renderMembersColumn(item.members, item.members_count);
        case 'my_group':
            return renderMyGroupColumn(item.my_group);
        default:
            return (
                <div key={column.key}>
                    {getKeyValue(item, column.key)}
                </div>
            );
    }
};
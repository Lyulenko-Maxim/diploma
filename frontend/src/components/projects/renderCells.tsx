import {Avatar, AvatarGroup, Chip, getKeyValue, User} from "@nextui-org/react";
import {CameraOff, Circle} from "lucide-react";
import React from "react";
import {IProfilePublic} from "@/types/user.types";
import {IProjectColumn, IMember, IDashboardProject} from "@/types/project.types";
import {IGroup} from "@/types/group.types";

const renderOwnerColumn = (owner: IProfilePublic) => {
    const {username, first_name, last_name, photo} = owner;
    return (
        <div>
            <User
                name={username}
                description={(first_name || '') + ' ' + (last_name || '')}
                avatarProps={{
                    isBordered: true,
                    src: photo || '',
                    fallback: <CameraOff/>
                }}
            />
        </div>
    );
};

const renderMembersColumn = (members: IMember[], members_count: number) => {
    return (
        <div>
            <AvatarGroup isBordered max={3} total={members_count} className="justify-start">
                {members.map((member) => {
                    const {photo, id} = member.profile;
                    return <Avatar key={id} src={photo || ''}/>;
                })}
            </AvatarGroup>
        </div>
    );
};

const renderMyGroupColumn = (currentMember: IMember) => {
    const {name, color_hex} = currentMember.highest_group;
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

export const renderCells = (item: IDashboardProject, column: IProjectColumn) => {
    switch (column.key) {
        case 'name':
            return item.project.name;
        case 'owner':
            return renderOwnerColumn(item.project.owner);
        case 'members':
            return renderMembersColumn(item.random_members, item.members_count);
        case 'my_group':
            return renderMyGroupColumn(item.current_member);
        default:
            return (
                <div key={column.key}>
                    {getKeyValue(item, column.key)}
                </div>
            );
    }
};
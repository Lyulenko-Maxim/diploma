export const PERMISSIONS = {
    ADMINISTRATOR: 'admin',
    MANAGE_PROJECT: 'manage_project',
    MANAGE_GROUPS: 'manage_groups',
    MANAGE_MEMBERS: 'manage_members',
    MANAGE_TASKS: 'manage_tasks',
    MANAGE_STATUSES: 'manage_statuses',
    MANAGE_MARKERS: 'manage_markers',
    MANAGE_COMMENTS: 'manage_comments',
    CREATE_COMMENTS: 'create_comments',
    CREATE_INVITATIONS: 'create_invitations'
};
export type Permission = typeof PERMISSIONS[keyof typeof PERMISSIONS];

export const checkPermissions = (memberPermissionsCodes: Permission[], requiredPermissionsCodes: Permission[]) => {
    return requiredPermissionsCodes.some(permission => memberPermissionsCodes.includes(permission));
};
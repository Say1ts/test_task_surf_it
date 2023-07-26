INSERT INTO role (role_name, description)
VALUES ('user', 'Regular user with basic permissions'),
       ('admin', 'Administrator with all permissions'),
       ('moderator', 'Moderator with advanced permissions');

INSERT INTO permission (title, description)
VALUES ('delete_ads', 'Permission to delete ads'),
       ('delete_review', 'Permission to delete reviews'),
       ('delete_complain', 'Permission to delete complaints'),
       ('make_admin', 'Permission to promote a user to an admin'),
       ('view_complaints', 'Permission to view complaints'),
       ('ban_user', 'Permission to ban users'),
       ('unban_user', 'Permission to unban users'),
       ('base_permissions', 'Base permissions for a regular user'),
       ('edit_ads', 'Permission to edit ads');

-- Adding base_permissions and edit_ads to user
INSERT INTO user_role_permission (role_id, permission_id)
SELECT role.id, permission.id
FROM role, permission
WHERE role.role_name = 'user'
AND permission.title IN ('base_permissions');

-- Adding all permissions to admin
INSERT INTO user_role_permission (role_id, permission_id)
SELECT role.id, permission.id
FROM role, permission
WHERE role.role_name = 'admin';

-- Adding specific permissions to moderator
INSERT INTO user_role_permission (role_id, permission_id)
SELECT role.id, permission.id
FROM role, permission
WHERE role.role_name = 'moderator'
AND permission.title IN ('delete_ads', 'delete_review', 'delete_complain', 'view_complaints');

/**
 * User service API
 * API description in Markdown.
 *
 * OpenAPI spec version: 1.0.0
 *
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
import { RoleType } from './roleType'
import { UserType } from './userType'


export interface CommonUserInfo
{
    id: number;
    username: string;
    role: RoleType;
    type: UserType;
}
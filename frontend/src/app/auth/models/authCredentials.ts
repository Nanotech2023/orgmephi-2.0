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

export interface AuthCredentials
{
    /**
     * Email for external users, username for MEPhI students, number for unconfirmed users
     */
    username: string;
    password: string;
}
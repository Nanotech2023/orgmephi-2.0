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
import { PersonalInfo } from './personalInfo'
import { RegisterAuthInfo } from './registerAuthInfo'
import { RegisterConfirm } from './registerConfirm'
import { StudentInfo } from './studentInfo'
import { UserType } from './userType'


export interface Registration
{
    authInfo: RegisterAuthInfo;
    personalInfo: PersonalInfo;
    registerType: UserType;
    studentInfo?: StudentInfo;
    registerConfirm: RegisterConfirm;
}
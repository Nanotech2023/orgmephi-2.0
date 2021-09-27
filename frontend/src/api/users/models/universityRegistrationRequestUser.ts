/**
 * aggregate_user
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { RegistrationInfoUser } from './registrationInfoUser';
import { RegistrationStudentInfoUser } from './registrationStudentInfoUser';
import { RegistrationPersonalInfoUser } from './registrationPersonalInfoUser';


export interface UniversityRegistrationRequestUser { 
    auth_info: RegistrationInfoUser;
    captcha?: string;
    personal_info: RegistrationPersonalInfoUser;
    register_type: UniversityRegistrationRequestUser.RegisterTypeEnum;
    student_info: RegistrationStudentInfoUser;
}
export namespace UniversityRegistrationRequestUser {
    export type RegisterTypeEnum = 'University';
    export const RegisterTypeEnum = {
        University: 'University' as RegisterTypeEnum
    };
}



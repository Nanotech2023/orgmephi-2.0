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
import { TypeCommonName } from './typeCommonName';
import { TypeDate } from './typeDate';
import { TypePhone } from './typePhone';

export interface TypeStudentInfo { 
    phoneNumber?: TypePhone;
    university?: TypeCommonName;
    admissionYear?: TypeDate;
    universityCountry?: TypeCommonName;
    citizenship?: TypeCommonName;
    region?: TypeCommonName;
    city?: TypeCommonName;
}
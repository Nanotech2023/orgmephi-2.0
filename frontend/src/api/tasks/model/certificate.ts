/**
 * aggregate_contest_tasks
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


export interface Certificate { 
    certificate_category: Certificate.CertificateCategoryEnum;
    readonly certificate_id?: number;
    readonly certificate_type_id: number;
    /**
     * Academic year of the certificate
     */
    certificate_year: number;
    /**
     * Maximum amount of lines
     */
    max_lines?: number | null;
    /**
     * #rrggbbaa color code
     */
    text_color?: string;
    /**
     * Font size
     */
    text_size?: number;
    /**
     * Distance between lines
     */
    text_spacing?: number;
    /**
     * Text font, see /contest/tasks/admin/fonts for available fonts
     */
    text_style?: string;
    /**
     * Textbox width
     */
    text_width: number;
    /**
     * Left border of textbox
     */
    text_x: number;
    /**
     * Bottom border of first line of text
     */
    text_y: number;
}
export namespace Certificate {
    export type CertificateCategoryEnum = 'Winner 1' | 'Winner 2' | 'Winner 3' | 'Diploma 1' | 'Diploma 2' | 'Diploma 3' | 'Participant';
    export const CertificateCategoryEnum = {
        Winner1: 'Winner 1' as CertificateCategoryEnum,
        Winner2: 'Winner 2' as CertificateCategoryEnum,
        Winner3: 'Winner 3' as CertificateCategoryEnum,
        Diploma1: 'Diploma 1' as CertificateCategoryEnum,
        Diploma2: 'Diploma 2' as CertificateCategoryEnum,
        Diploma3: 'Diploma 3' as CertificateCategoryEnum,
        Participant: 'Participant' as CertificateCategoryEnum
    };
}



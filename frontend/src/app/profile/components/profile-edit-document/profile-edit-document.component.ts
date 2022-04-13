import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Document, DocumentTypeEnum } from '@api/users/models'
import { getDocumentDisplay } from '@/shared/localizeUtils'


@Component( {
    selector: 'app-profile-edit-document',
    templateUrl: './profile-edit-document.component.html',
    styleUrls: [ './profile-edit-document.component.scss' ]
} )
export class ProfileEditDocumentComponent
{
    @Input() model!: Document
    @Output() modelChange = new EventEmitter<Document>()

    readonly documentTypes: DocumentTypeEnum[] = [
        DocumentTypeEnum.RfPassport,
        DocumentTypeEnum.RfInternationalPassport,
        DocumentTypeEnum.BirthCertificate,
        DocumentTypeEnum.ForeignPassport,
        DocumentTypeEnum.OtherDocument
    ]

    getDocumentDisplay( documentType: DocumentTypeEnum ): string
    {
        return getDocumentDisplay( documentType )
    }
}
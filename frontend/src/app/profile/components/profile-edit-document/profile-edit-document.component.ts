import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Document, Location } from '@api/users/models'
import { DocumentTypeEnum } from '@api/users/models/documentType'


@Component( {
    selector: 'app-profile-edit-document',
    templateUrl: './profile-edit-document.component.html',
    styleUrls: [ './profile-edit-document.component.scss' ]
} )
export class ProfileEditDocumentComponent
{
    @Input() model!: Document | undefined
    @Output() modelChange = new EventEmitter<Document>()
    document: Document = this.model ?? this.getEmptyDocument()

    onModelChange( $event: Document )
    {
        this.modelChange.emit( $event )
    }

    getEmptyDocument(): Document
    {
        return {
            document_name: undefined,
            document_type: DocumentTypeEnum.RfPassport,
            issue_date: undefined,
            issuer: undefined,
            number: undefined,
            series: undefined,
            code: undefined,
            user_id: undefined
        }
    }
}
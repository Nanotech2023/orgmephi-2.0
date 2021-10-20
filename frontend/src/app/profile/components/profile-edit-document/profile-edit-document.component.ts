import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { Document, Location } from '@api/users/models'
import { DocumentTypeEnum } from '@api/users/models/documentType'


@Component( {
    selector: 'app-profile-edit-document',
    templateUrl: './profile-edit-document.component.html',
    styleUrls: [ './profile-edit-document.component.scss' ]
} )
export class ProfileEditDocumentComponent implements OnInit
{
    @Input() model!: Document | undefined
    @Output() modelChange = new EventEmitter<Document>()
    document!: Document

    ngOnInit(): void
    {
        this.document = this.model!
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.document )
    }

}